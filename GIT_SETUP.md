# Git Setup Guide

## Initialize Repository

```bash
cd "c:\Users\Loja Miguel\Documents\MEGA\riqueza"

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "feat: PR1 - MVP Generator + Sample Posts + Tests

- Content generator core (700-1200 words, SEO-optimized)
- LGPD-compliant database models (privacy-first)
- Security infrastructure (Argon2, AES-256, JWT)
- Test suite with >= 75% coverage
- Comprehensive documentation (LGPD, security, DPA)
- Docker Compose full stack
- GitHub Actions CI/CD pipeline
- 15 seed keywords + scripts
- Setup automation (setup.ps1, setup.sh)

Implements:
✅ Privacy by Design (hashed IPs, consent tracking)
✅ Security First (Argon2, AES-256, JWT)
✅ Ethical content generation (originality checking)
✅ Human review workflow (review_required=true)
✅ Kill-switch mechanism
✅ Free-tier infrastructure ready

BREAKING CHANGE: Initial commit - establishes project foundation"

# Set main branch
git branch -M main
```

## Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `autocash-ultimate`
3. Description: `Privacy-first, ethical content monetization ecosystem - LGPD compliant, zero investment startup`
4. Visibility: Private (recommended) or Public
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/autocash-ultimate.git

# Push main branch
git push -u origin main
```

## Create PR1 Branch and Pull Request

```bash
# Create feature branch
git checkout -b feature/pr1-mvp-generator

# Push feature branch
git push -u origin feature/pr1-mvp-generator

# Now go to GitHub and create Pull Request from feature/pr1-mvp-generator to main
```

### PR Details

**Title**: `PR1: MVP Generator + Sample Posts + Tests`

**Description**: Copy content from `PR1_DESCRIPTION.md`

**Labels**: 
- `enhancement`
- `mvp`
- `documentation`
- `security`

**Reviewers**: Add yourself or team members

## Configure GitHub Settings

### Enable GitHub Actions

1. Go to repo Settings → Actions → General
2. Allow all actions and reusable workflows
3. Save

### Add GitHub Secrets (Optional for CI)

Settings → Secrets and variables → Actions → New repository secret:

- `CODECOV_TOKEN` (optional, for coverage reports)

### Enable Dependabot (Recommended)

Settings → Security → Dependabot:
- Enable Dependabot alerts
- Enable Dependabot security updates

### Branch Protection (Recommended for Production)

Settings → Branches → Add rule:

**Branch name pattern**: `main`

Protect matching branches:
- [x] Require a pull request before merging
- [x] Require status checks to pass before merging
  - Search for: `lint`, `security`, `test`, `build`
- [x] Require conversation resolution before merging
- [ ] Require signed commits (optional)
- [x] Include administrators

## Commit Message Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Maintain, build process, etc.
- `security`: Security fix
- `ci`: CI/CD changes

**Examples**:

```bash
# Feature
git commit -m "feat(generator): add multi-language support"

# Bug fix
git commit -m "fix(tracking): resolve duplicate event logging"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Security
git commit -m "security(auth): implement rate limiting on login"
```

## .gitignore Already Configured

The `.gitignore` file already excludes:
- ✅ Secrets (`.env`, `*.key`, `credentials.json`)
- ✅ Data files (`*.db`, `data/`)
- ✅ Logs (`logs/`, `*.log`)
- ✅ Python cache (`__pycache__/`, `*.pyc`)
- ✅ Virtual environments (`venv/`, `.venv/`)
- ✅ IDE files (`.vscode/`, `.idea/`)
- ✅ Build artifacts (`dist/`, `build/`)

**NEVER COMMIT**:
- Secrets or credentials
- Database files with real data
- API keys
- User data (LGPD!)
- Large binary files

## Verify Before Push

```bash
# Check what will be committed
git status

# Review changes
git diff

# Check for secrets (IMPORTANT!)
git secrets --scan  # If you have git-secrets installed

# Or manually search
grep -r "password\|secret\|key" . --exclude-dir=.git --exclude-dir=venv --exclude-dir=node_modules
```

## Emergency: Accidentally Committed Secrets

**If you committed secrets to local repo (not pushed):**

```bash
# Undo last commit (keep changes)
git reset HEAD~1

# Remove .env from staging
git reset .env

# Add .env to .gitignore if not already
echo ".env" >> .gitignore

# Commit again without secrets
git add .
git commit -m "your commit message"
```

**If you pushed secrets to GitHub:**

1. **IMMEDIATELY** rotate/revoke the exposed secrets
2. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```
3. Change all secrets in production
4. Review GitHub commit history to verify removal
5. Consider repo as compromised; rotate ALL credentials

---

**Next Steps After Git Setup**:
1. ✅ Repository created and pushed
2. ✅ PR1 branch created
3. Run `.\setup.ps1` to test locally
4. Create Pull Request on GitHub
5. Review PR1_DESCRIPTION.md
6. Merge when ready!
