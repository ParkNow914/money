"""
Batch generation routes for automated content creation.

Allows generating multiple articles at once.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.config import settings
from app.db import get_db
from app.models import Article, Keyword
from app.services.generator import generator
from app.routes.generate import verify_admin_token

router = APIRouter()


class BatchGenerateRequest(BaseModel):
    """Request to generate multiple articles."""
    count: int = 5
    review_required: Optional[bool] = None
    use_unused_keywords: bool = True


class BatchGenerateResponse(BaseModel):
    """Response from batch generation."""
    success: bool
    total_requested: int
    generated: int
    failed: int
    articles: List[dict]
    message: str


def generate_articles_batch(
    count: int,
    review_required: bool,
    use_unused_keywords: bool,
    db: Session
) -> dict:
    """
    Generate multiple articles in batch.
    
    This function is executed in the background.
    """
    generated = []
    failed = []
    
    # Get keywords to use
    query = db.query(Keyword).order_by(Keyword.priority.desc())
    
    if use_unused_keywords:
        query = query.filter(Keyword.used == False)
    
    keywords = query.limit(count).all()
    
    if not keywords:
        return {
            "success": False,
            "generated": 0,
            "failed": count,
            "message": "No keywords available for generation"
        }
    
    for keyword_obj in keywords:
        try:
            # Check if article already exists
            existing = db.query(Article).filter(
                Article.keyword == keyword_obj.keyword
            ).first()
            
            if existing:
                failed.append({
                    "keyword": keyword_obj.keyword,
                    "reason": "Article already exists"
                })
                continue
            
            # Generate article
            article = generator.generate_article(keyword_obj.keyword)
            
            if review_required is not None:
                article.review_required = review_required
            
            # Validate
            is_valid, errors = generator.validate_article(article)
            
            if not is_valid:
                failed.append({
                    "keyword": keyword_obj.keyword,
                    "reason": f"Validation failed: {', '.join(errors)}"
                })
                continue
            
            # Save to database
            db.add(article)
            
            # Mark keyword as used
            keyword_obj.used = True
            keyword_obj.used_at = datetime.utcnow()
            
            db.commit()
            db.refresh(article)
            
            generated.append({
                "id": article.id,
                "slug": article.slug,
                "title": article.title,
                "keyword": article.keyword,
                "word_count": article.word_count,
                "status": article.status.value
            })
            
        except Exception as e:
            db.rollback()
            failed.append({
                "keyword": keyword_obj.keyword,
                "reason": str(e)
            })
    
    return {
        "success": len(generated) > 0,
        "generated": len(generated),
        "failed": len(failed),
        "articles": generated,
        "errors": failed if failed else None
    }


@router.post("/batch-generate", response_model=BatchGenerateResponse)
async def batch_generate(
    request: BatchGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Generate multiple articles in batch.
    
    Requires admin authorization.
    Use for automated content generation via cron/workers.
    """
    if request.count < 1 or request.count > 50:
        raise HTTPException(
            status_code=400,
            detail="Count must be between 1 and 50"
        )
    
    # Check kill switch
    if settings.KILL_SWITCH_ENABLED:
        raise HTTPException(
            status_code=503,
            detail="Service paused - kill switch enabled"
        )
    
    # Use default review_required if not specified
    review_required = request.review_required if request.review_required is not None else settings.REVIEW_REQUIRED
    
    # Execute batch generation
    result = generate_articles_batch(
        count=request.count,
        review_required=review_required,
        use_unused_keywords=request.use_unused_keywords,
        db=db
    )
    
    return BatchGenerateResponse(
        success=result["success"],
        total_requested=request.count,
        generated=result["generated"],
        failed=result["failed"],
        articles=result["articles"],
        message=f"Generated {result['generated']} articles, {result['failed']} failed"
    )


@router.get("/batch-status")
async def batch_status(
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Get status of batch generation capabilities.
    
    Returns available keywords and system readiness.
    """
    from sqlalchemy import func
    
    total_keywords = db.query(func.count(Keyword.id)).scalar() or 0
    unused_keywords = db.query(func.count(Keyword.id)).filter(
        Keyword.used == False
    ).scalar() or 0
    
    return {
        "ready": not settings.KILL_SWITCH_ENABLED,
        "kill_switch": settings.KILL_SWITCH_ENABLED,
        "review_required": settings.REVIEW_REQUIRED,
        "keywords": {
            "total": total_keywords,
            "unused": unused_keywords,
            "available_for_batch": unused_keywords
        },
        "limits": {
            "min_batch_size": 1,
            "max_batch_size": 50
        }
    }
