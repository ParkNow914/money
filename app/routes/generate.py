"""
Content generation API routes.

Endpoints for generating, managing, and retrieving articles.
All generation respects review_required flag for ethical content approval.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import Article, ContentStatus, Keyword
from app.services.generator import generator

router = APIRouter()


class GenerateRequest(BaseModel):
    """Request to generate article from keyword."""
    keyword: str = Field(..., min_length=2, max_length=255)
    review_required: Optional[bool] = None


class GenerateResponse(BaseModel):
    """Response from article generation."""
    success: bool
    article_id: Optional[int] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    word_count: Optional[int] = None
    review_required: Optional[bool] = None
    message: str


class ArticleResponse(BaseModel):
    """Article data response."""
    id: int
    slug: str
    keyword: str
    title: str
    meta_description: Optional[str]
    body_html: str
    body_plain: str
    word_count: int
    headings: List[dict]
    internal_links: List[dict]
    tags: List[str]
    status: str
    review_required: bool
    created_at: str
    published_at: Optional[str]
    
    class Config:
        from_attributes = True


def verify_admin_token(authorization: str = Header(None)) -> bool:
    """Verify admin token for protected endpoints."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = parts[1]
    if token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    
    return True


@router.post("/generate", response_model=GenerateResponse)
async def generate_article(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Generate a new article from a keyword.
    
    Requires admin authorization.
    Generated articles are in DRAFT status by default and require review.
    """
    try:
        # Check if article already exists for this keyword
        existing = db.query(Article).filter(Article.keyword == request.keyword).first()
        if existing:
            return GenerateResponse(
                success=False,
                message=f"Article already exists for keyword: {request.keyword}",
                article_id=existing.id,
                slug=existing.slug,
            )
        
        # Generate article
        article = generator.generate_article(request.keyword)
        
        # Override review_required if specified
        if request.review_required is not None:
            article.review_required = request.review_required
        
        # Validate article
        is_valid, errors = generator.validate_article(article)
        if not is_valid:
            return GenerateResponse(
                success=False,
                message=f"Article validation failed: {', '.join(errors)}"
            )
        
        # Save to database
        db.add(article)
        db.commit()
        db.refresh(article)
        
        return GenerateResponse(
            success=True,
            article_id=article.id,
            slug=article.slug,
            title=article.title,
            status=article.status.value,
            word_count=article.word_count,
            review_required=article.review_required,
            message="Article generated successfully"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/articles", response_model=List[ArticleResponse])
async def list_articles(
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List articles with optional status filter.
    
    Public endpoint - returns basic article information.
    """
    query = db.query(Article)
    
    if status:
        try:
            status_enum = ContentStatus(status)
            query = query.filter(Article.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    articles = query.order_by(Article.created_at.desc()).offset(offset).limit(limit).all()
    
    return [
        ArticleResponse(
            id=a.id,
            slug=a.slug,
            keyword=a.keyword,
            title=a.title,
            meta_description=a.meta_description,
            body_html=a.body_html,
            body_plain=a.body_plain,
            word_count=a.word_count,
            headings=a.headings,
            internal_links=a.internal_links,
            tags=a.tags,
            status=a.status.value,
            review_required=a.review_required,
            created_at=a.created_at.isoformat(),
            published_at=a.published_at.isoformat() if a.published_at else None,
        )
        for a in articles
    ]


@router.get("/articles/{slug}", response_model=ArticleResponse)
async def get_article(slug: str, db: Session = Depends(get_db)):
    """Get a specific article by slug."""
    article = db.query(Article).filter(Article.slug == slug).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return ArticleResponse(
        id=article.id,
        slug=article.slug,
        keyword=article.keyword,
        title=article.title,
        meta_description=article.meta_description,
        body_html=article.body_html,
        body_plain=article.body_plain,
        word_count=article.word_count,
        headings=article.headings,
        internal_links=article.internal_links,
        tags=article.tags,
        status=article.status.value,
        review_required=article.review_required,
        created_at=article.created_at.isoformat(),
        published_at=article.published_at.isoformat() if article.published_at else None,
    )


@router.post("/keywords/seed")
async def seed_keyword(
    keyword: str,
    priority: int = 5,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Add a keyword to the seed list.
    
    Requires admin authorization.
    """
    # Check if keyword already exists
    existing = db.query(Keyword).filter(Keyword.keyword == keyword).first()
    if existing:
        return {"success": False, "message": "Keyword already exists"}
    
    # Create keyword
    kw = Keyword(keyword=keyword, priority=priority)
    db.add(kw)
    db.commit()
    db.refresh(kw)
    
    return {
        "success": True,
        "keyword_id": kw.id,
        "keyword": kw.keyword,
        "message": "Keyword added successfully"
    }


@router.get("/keywords")
async def list_keywords(
    used: Optional[bool] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    List keywords.
    
    Requires admin authorization.
    """
    query = db.query(Keyword)
    
    if used is not None:
        query = query.filter(Keyword.used == used)
    
    keywords = query.order_by(Keyword.priority.desc()).limit(limit).all()
    
    return {
        "keywords": [
            {
                "id": k.id,
                "keyword": k.keyword,
                "priority": k.priority,
                "used": k.used,
            }
            for k in keywords
        ]
    }
