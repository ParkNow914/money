# 📋 PR2 PLAN - Publisher + Static Site Generation

**Projeto:** AutoCash Ultimate  
**PR:** #2 - Publisher + Static Site  
**Dependências:** PR1 (MVP Generator) ✅  
**Tempo estimado:** 1-2 semanas  
**Prioridade:** 🔴 ALTA

---

## 🎯 OBJETIVO

Criar sistema completo de publicação de conteúdo com site estático otimizado para SEO, deploy automático no GitHub Pages, e capacidade de monetização via links de afiliados.

---

## 📊 COMPONENTES PRINCIPAIS

### 1. Frontend (Next.js 14)

```
/site
├── app/                       # App Router (Next.js 14)
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Homepage
│   ├── [slug]/
│   │   └── page.tsx          # Dynamic article pages
│   ├── category/
│   │   └── [category]/
│   │       └── page.tsx      # Category pages
│   ├── sitemap.xml/
│   │   └── route.ts          # Dynamic sitemap
│   └── rss.xml/
│       └── route.ts          # RSS feed
├── components/
│   ├── Article.tsx           # Article component
│   ├── ArticleList.tsx       # Article list
│   ├── CategoryNav.tsx       # Category navigation
│   ├── Footer.tsx            # Footer with legal links
│   ├── Header.tsx            # Header/navigation
│   └── SEO.tsx               # SEO meta tags
├── lib/
│   ├── api.ts                # API client (fetch articles)
│   ├── analytics.ts          # Matomo integration
│   └── affiliate.ts          # Affiliate link tracking
├── public/
│   ├── robots.txt            # SEO robots
│   └── ads.txt               # AdSense verification
├── styles/
│   └── globals.css           # Tailwind CSS
├── next.config.js            # Next.js config (SSG, output: export)
├── package.json              # Dependencies
└── tsconfig.json             # TypeScript config
```

#### Tecnologias
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Language:** TypeScript
- **Rendering:** SSG (Static Site Generation) + ISR
- **Deploy:** GitHub Pages via GitHub Actions

---

### 2. Publisher Service

```python
# app/services/publisher.py

class StaticSitePublisher:
    """
    Generate static HTML from articles in database
    """
    
    def publish_article(self, article_id: int) -> Path:
        """Generate static HTML for single article"""
        pass
    
    def publish_all(self) -> int:
        """Generate static site for all published articles"""
        pass
    
    def generate_sitemap(self) -> Path:
        """Generate sitemap.xml"""
        pass
    
    def generate_rss(self) -> Path:
        """Generate RSS feed"""
        pass
    
    def optimize_images(self) -> None:
        """Optimize images for web"""
        pass
```

---

### 3. SEO Optimization

#### JSON-LD Schemas (já temos!)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "description": "...",
  "author": {
    "@type": "Organization",
    "name": "AutoCash Ultimate"
  },
  "datePublished": "...",
  "dateModified": "...",
  "image": "...",
  "publisher": {
    "@type": "Organization",
    "name": "AutoCash Ultimate",
    "logo": {
      "@type": "ImageObject",
      "url": "..."
    }
  }
}
```

#### Meta Tags
```tsx
// components/SEO.tsx
export function SEO({ article }) {
  return (
    <Head>
      <title>{article.title}</title>
      <meta name="description" content={article.meta_description} />
      <meta property="og:title" content={article.title} />
      <meta property="og:description" content={article.meta_description} />
      <meta property="og:type" content="article" />
      <meta property="og:url" content={`https://yourdomain.com/${article.slug}`} />
      <meta name="twitter:card" content="summary_large_image" />
      <link rel="canonical" href={`https://yourdomain.com/${article.slug}`} />
    </Head>
  )
}
```

#### robots.txt
```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: https://yourdomain.com/sitemap.xml
```

#### sitemap.xml (dinâmico)
```typescript
// app/sitemap.xml/route.ts
export async function GET() {
  const articles = await getPublishedArticles()
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      ${articles.map(article => `
        <url>
          <loc>https://yourdomain.com/${article.slug}</loc>
          <lastmod>${article.updated_at}</lastmod>
          <changefreq>weekly</changefreq>
          <priority>0.8</priority>
        </url>
      `).join('')}
    </urlset>`
  
  return new Response(sitemap, {
    headers: { 'Content-Type': 'application/xml' }
  })
}
```

---

### 4. GitHub Pages Deploy

#### GitHub Actions Workflow
```yaml
# .github/workflows/deploy-site.yml
name: Deploy Site

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: site/package-lock.json
    
    - name: Install dependencies
      working-directory: ./site
      run: npm ci
    
    - name: Build Next.js site
      working-directory: ./site
      run: |
        npm run build
        touch out/.nojekyll
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site/out
        cname: yourdomain.com  # opcional: custom domain
```

#### next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,  // GitHub Pages não suporta Image Optimization
  },
  basePath: process.env.GITHUB_ACTIONS ? '/money' : '',
  assetPrefix: process.env.GITHUB_ACTIONS ? '/money/' : '',
}

module.exports = nextConfig
```

---

### 5. Analytics (Privacy-First)

#### Matomo Integration
```typescript
// lib/analytics.ts
export const trackPageView = (url: string) => {
  if (typeof window !== 'undefined' && window._paq) {
    window._paq.push(['setCustomUrl', url])
    window._paq.push(['trackPageView'])
  }
}

export const trackEvent = (category: string, action: string, name?: string) => {
  if (typeof window !== 'undefined' && window._paq) {
    window._paq.push(['trackEvent', category, action, name])
  }
}

export const trackAffiliateClick = (articleId: number, affiliateId: string) => {
  trackEvent('Affiliate', 'Click', `${articleId}-${affiliateId}`)
}
```

---

### 6. Affiliate Link Tracking

#### Automatic UTM Injection
```typescript
// lib/affiliate.ts
export function injectUTM(url: string, article: Article): string {
  const params = new URLSearchParams({
    utm_source: 'autocash-ultimate',
    utm_medium: 'article',
    utm_campaign: article.slug,
    utm_content: article.id.toString(),
  })
  
  return `${url}?${params.toString()}`
}

export function trackClick(articleId: number, url: string) {
  // Send to backend API
  fetch('/api/tracking/click', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ article_id: articleId, url }),
  })
}
```

---

## 📦 DELIVERABLES

### Código
- [ ] Next.js 14 app completo com SSG
- [ ] Componentes React reutilizáveis
- [ ] Publisher service Python
- [ ] GitHub Actions workflow de deploy
- [ ] Configuração de GitHub Pages

### Documentação
- [ ] README do site (site/README.md)
- [ ] Guia de customização de tema
- [ ] Guia de deploy manual
- [ ] Troubleshooting comum

### Testes
- [ ] Unit tests para publisher service
- [ ] E2E tests com Playwright
- [ ] Lighthouse CI (performance >= 90)

---

## 🎯 FEATURES

### MVP (obrigatório)
- [x] Site Next.js 14 com SSG
- [x] Homepage com lista de artigos
- [x] Páginas dinâmicas de artigos
- [x] SEO otimizado (meta tags, JSON-LD)
- [x] Sitemap.xml dinâmico
- [x] robots.txt
- [x] Deploy automático GitHub Pages
- [x] Responsive design (mobile-first)

### Nice to Have (opcional)
- [ ] RSS feed
- [ ] Categorias/tags
- [ ] Busca client-side (Fuse.js)
- [ ] Dark mode
- [ ] Comentários (Giscus/Disqus)
- [ ] Related articles
- [ ] Table of contents
- [ ] Reading time estimate
- [ ] Social share buttons

---

## 🔧 SETUP LOCAL

### Pré-requisitos
```bash
# Node.js 20+
node --version

# npm
npm --version
```

### Instalação
```bash
# Criar diretório do site
mkdir site
cd site

# Inicializar Next.js
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir

# Instalar dependências adicionais
npm install @heroicons/react date-fns gray-matter
npm install -D @types/node
```

### Desenvolvimento
```bash
# Rodar dev server
npm run dev

# Build para produção
npm run build

# Preview build
npm run start
```

---

## 🚀 DEPLOYMENT

### GitHub Pages

1. **Habilitar GitHub Pages**
   - Settings > Pages
   - Source: GitHub Actions

2. **Configurar Custom Domain (opcional)**
   - Settings > Pages > Custom domain
   - Adicionar CNAME: `yourdomain.com`
   - Configurar DNS:
     ```
     Type: CNAME
     Name: www
     Value: parknow914.github.io
     ```

3. **Deploy**
   ```bash
   # Push para main automaticamente deploya
   git push origin main
   ```

---

## 📊 MÉTRICAS DE SUCESSO

| Métrica | Objetivo |
|---------|----------|
| **Lighthouse Performance** | >= 90 |
| **Lighthouse SEO** | 100 |
| **Lighthouse Accessibility** | >= 90 |
| **Time to First Byte** | < 600ms |
| **First Contentful Paint** | < 1.8s |
| **Largest Contentful Paint** | < 2.5s |
| **Cumulative Layout Shift** | < 0.1 |
| **Total Blocking Time** | < 200ms |

---

## 🎨 DESIGN SYSTEM

### Cores
```css
:root {
  --primary: #3b82f6;      /* Blue */
  --secondary: #8b5cf6;    /* Purple */
  --accent: #10b981;       /* Green */
  --background: #ffffff;
  --foreground: #1f2937;
  --muted: #6b7280;
}
```

### Tipografia
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

h1: 2.5rem / 600
h2: 2rem / 600
h3: 1.5rem / 600
body: 1rem / 400
small: 0.875rem / 400
```

---

## 🔗 INTEGRATIONS

### Google Search Console
1. Verificar propriedade (meta tag ou DNS)
2. Submeter sitemap.xml
3. Configurar país-alvo: Brasil
4. Monitorar indexação

### Google Analytics / Matomo
```typescript
// Matomo (privacy-first)
<script>
  var _paq = window._paq = window._paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  // ...
</script>
```

### Cloudflare (opcional)
- CDN para performance
- DDoS protection
- SSL/TLS
- Analytics

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Setup (Dia 1-2)
- [ ] Criar diretório `/site`
- [ ] Setup Next.js 14 + TypeScript
- [ ] Configurar Tailwind CSS
- [ ] Criar componentes base (Header, Footer, Layout)
- [ ] Configurar next.config.js para SSG

### Fase 2: Core (Dia 3-5)
- [ ] Implementar Homepage
- [ ] Implementar página de artigo dinâmica
- [ ] Implementar SEO component
- [ ] Criar API client para buscar artigos
- [ ] Implementar sitemap.xml dinâmico
- [ ] Adicionar robots.txt

### Fase 3: Publisher (Dia 6-7)
- [ ] Implementar publisher.py service
- [ ] Criar comando CLI para publicação
- [ ] Testar geração de site estático
- [ ] Validar HTML gerado

### Fase 4: Deploy (Dia 8-9)
- [ ] Criar GitHub Actions workflow
- [ ] Configurar GitHub Pages
- [ ] Testar deploy automático
- [ ] Configurar custom domain (opcional)

### Fase 5: Testing (Dia 10-11)
- [ ] Unit tests para publisher
- [ ] E2E tests com Playwright
- [ ] Lighthouse CI
- [ ] Testes de SEO

### Fase 6: Docs (Dia 12-14)
- [ ] Escrever README do site
- [ ] Guia de customização
- [ ] Guia de deploy
- [ ] Troubleshooting

---

## 🆘 PROBLEMAS COMUNS

### Build falha no GitHub Actions
**Causa:** Node version incompatível  
**Solução:** Usar Node 20 LTS no workflow

### Imagens não carregam
**Causa:** Next.js Image Optimization não funciona no SSG  
**Solução:** `images: { unoptimized: true }`

### Links quebrados com basePath
**Causa:** basePath não configurado corretamente  
**Solução:** Usar `process.env.GITHUB_ACTIONS` para detectar CI

### Sitemap não aparece no Google
**Causa:** Não submetido no Search Console  
**Solução:** Submeter manualmente em Search Console

---

## ⏭️ PRÓXIMO PASSO

Após completar PR2:
- **PR3:** Tracking & Analytics (Matomo, eventos, conversões)
- **PR4:** Monetization (links de afiliados, ads, tracking de receita)
- **PR5:** Repurposer (threads X, vídeo scripts, PDFs)

---

**Data de criação:** 21 de outubro de 2025  
**Status:** 📋 Planejamento  
**Próxima ação:** Começar implementação após merge do PR1
