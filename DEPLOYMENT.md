# Nexus AI OS - Complete Deployment Guide

## 🚀 Production Deployment Workflow

This guide covers complete deployment from local development to production cloud deployment.

---

## 📋 Pre-Deployment Checklist

### Required Accounts & Keys
- [ ] Google AI API Key ([Get here](https://ai.google.dev/))
- [ ] GitHub account for code repository
- [ ] Cloud platform account (choose one):
  - Railway.app (Recommended - easiest)
  - Render.com (Good alternative)
  - Google Cloud Platform (Enterprise)
  - AWS (Enterprise)
  - Azure (Enterprise)

### Local Requirements
- [ ] Docker Desktop installed and running
- [ ] Git installed
- [ ] Node.js 20+ installed (for frontend)
- [ ] Python 3.11+ installed (for backend)

---

## 🔧 Local Development Setup

### Step 1: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/nexus-ai-os.git
cd nexus-ai-os

# Create environment file
cp .env.example .env

# Edit .env and add your keys
# Required: GOOGLE_API_KEY
# Optional: Modify database passwords for production
```

### Step 2: Start with Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Wait for "Nexus AI OS v1.0.0 started" message

# Verify services
docker-compose ps
# All services should show "Up" status
```

### Step 3: Verify Installation

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0","environment":"development"}

# Access interfaces:
# - API Docs: http://localhost:8000/docs
# - Neo4j: http://localhost:7474 (neo4j/nexus_graph_password)
# - Frontend: http://localhost:3000 (when implemented)
```

### Step 4: Test Core Functionality

```bash
# Create test agent
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "type": "sales",
    "description": "Test agent for verification",
    "capabilities": ["testing"]
  }'

# Should return agent details with ID

# Run test task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "agent_id": "auto",
    "task_type": "test",
    "description": "Test task execution",
    "priority": 5
  }'

# Should return task result
```

---

## 🏗️ Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start databases (Docker)
docker-compose up -d postgres redis neo4j qdrant

# Run database migrations (if needed)
# alembic upgrade head

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will be at http://localhost:5173
```

---

## 🌐 Cloud Deployment Options

### Option 1: Railway.app (Recommended - Easiest)

**Why Railway:**
- Free tier available
- Automatic HTTPS
- Easy database provisioning
- GitHub integration
- One-click deployment

**Steps:**

1. **Prepare Repository**
```bash
# Ensure code is pushed to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Deploy Backend**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Dockerfile

3. **Add Databases**
   - Click "New" → "Database" → "PostgreSQL"
   - Click "New" → "Database" → "Redis"
   - Note: Neo4j and Qdrant need custom deployment (see below)

4. **Configure Environment Variables**
   - In Railway dashboard, go to your service
   - Click "Variables"
   - Add all variables from `.env.example`
   - Railway auto-provides DATABASE_URL and REDIS_URL

5. **Deploy**
   - Railway automatically deploys on git push
   - Get your URL from Railway dashboard
   - Test: `https://your-app.railway.app/health`

**Neo4j on Railway:**
```bash
# Add Neo4j service
railway add neo4j

# Or use Neo4j Aura (cloud)
# https://neo4j.com/cloud/aura/
# Free tier available
```

### Option 2: Render.com

**Steps:**

1. **Create render.yaml**
```yaml
# Create this file in project root
services:
  - type: web
    name: nexus-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GOOGLE_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: nexus-db
          property: connectionString
      - key: REDIS_URL
        fromDatabase:
          name: nexus-redis
          property: connectionString

databases:
  - name: nexus-db
    databaseName: nexus
    user: nexus
  
  - name: nexus-redis
    type: redis
```

2. **Deploy**
   - Go to [render.com](https://render.com)
   - Click "New" → "Blueprint"
   - Connect GitHub repository
   - Render will use render.yaml
   - Add environment variables in dashboard

### Option 3: Google Cloud Platform (Enterprise)

**Architecture:**
- Cloud Run for backend (serverless)
- Cloud SQL for PostgreSQL
- Memorystore for Redis
- Compute Engine for Neo4j
- Cloud Storage for static files

**Steps:**

1. **Install Google Cloud SDK**
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

2. **Build and Push Container**
```bash
# Build backend image
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/nexus-backend

# Deploy to Cloud Run
gcloud run deploy nexus-backend \
  --image gcr.io/YOUR_PROJECT_ID/nexus-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key_here
```

3. **Set up Databases**
```bash
# Create Cloud SQL instance
gcloud sql instances create nexus-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1

# Create Redis instance
gcloud redis instances create nexus-redis \
  --size=1 \
  --region=us-central1
```

### Option 4: AWS (Enterprise)

**Architecture:**
- ECS Fargate for containers
- RDS for PostgreSQL
- ElastiCache for Redis
- EC2 for Neo4j
- S3 for static files
- CloudFront for CDN

**Steps:**

1. **Install AWS CLI**
```bash
# Install AWS CLI
# https://aws.amazon.com/cli/

# Configure
aws configure
```

2. **Create ECR Repository**
```bash
# Create repository
aws ecr create-repository --repository-name nexus-backend

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t nexus-backend backend/
docker tag nexus-backend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/nexus-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/nexus-backend:latest
```

3. **Deploy with ECS**
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name nexus-cluster

# Create task definition (see AWS docs)
# Deploy service
```

---

## 🔒 Production Environment Variables

### Required Variables

```bash
# Google AI
GOOGLE_API_KEY=your_actual_api_key_here

# Database (provided by cloud platform)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379
NEO4J_URI=bolt://host:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=secure_password_here
QDRANT_URL=http://host:6333

# Application
ENVIRONMENT=production
SECRET_KEY=generate_secure_random_key_here
CORS_ORIGINS=https://your-frontend-domain.com

# Security
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Logging
LOG_LEVEL=INFO
```

### Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate database passwords
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

---

## 🗄️ Database Migrations

### PostgreSQL Migrations

```bash
# Install Alembic (if not in requirements.txt)
pip install alembic

# Initialize Alembic (first time only)
cd backend
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Neo4j Initialization

```bash
# Connect to Neo4j
# Via browser: http://your-neo4j-host:7474

# Run initialization queries
CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT task_id IF NOT EXISTS FOR (t:Task) REQUIRE t.id IS UNIQUE;
CREATE INDEX agent_type IF NOT EXISTS FOR (a:Agent) ON (a.type);
CREATE INDEX task_type IF NOT EXISTS FOR (t:Task) ON (t.type);
```

---

## 🏗️ Build for Production

### Backend Build

```bash
cd backend

# Install production dependencies only
pip install --no-dev -r requirements.txt

# Run tests (if available)
pytest

# Build Docker image
docker build -t nexus-backend:latest .

# Test image locally
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  nexus-backend:latest
```

### Frontend Build

```bash
cd frontend

# Install dependencies
npm ci

# Build for production
npm run build

# Output will be in dist/
# Deploy dist/ to:
# - Vercel
# - Netlify
# - S3 + CloudFront
# - Cloud Storage + Cloud CDN
```

---

## 🔍 Health Checks & Monitoring

### Health Check Endpoints

```bash
# Basic health
GET /health
Response: {"status":"healthy","version":"1.0.0"}

# Detailed health (add this endpoint)
GET /health/detailed
Response: {
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "neo4j": "connected",
    "qdrant": "connected"
  },
  "uptime": 3600
}
```

### Monitoring Setup

**Option 1: Built-in Prometheus**
```python
# Add to requirements.txt
prometheus-client==0.19.0

# Add to main.py
from prometheus_client import make_asgi_app

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

**Option 2: Cloud Platform Monitoring**
- Railway: Built-in metrics
- Render: Built-in monitoring
- GCP: Cloud Monitoring
- AWS: CloudWatch
- Azure: Application Insights

**Option 3: External Services**
- Datadog
- New Relic
- Sentry (for error tracking)

---

## 🚦 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        run: |
          npm i -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Environment Secrets

Add to GitHub repository secrets:
- `RAILWAY_TOKEN`
- `GOOGLE_API_KEY`
- `DATABASE_URL`
- Other sensitive variables

---

## 📊 Performance Optimization

### Backend Optimizations

1. **Enable Caching**
```python
# Add Redis caching for frequent queries
from functools import lru_cache

@lru_cache(maxsize=100)
def get_agent_cached(agent_id: str):
    # Cache agent lookups
    pass
```

2. **Database Connection Pooling**
```python
# Already configured in database.py
# Adjust pool_size based on load
POOL_SIZE = 20
MAX_OVERFLOW = 10
```

3. **Async Optimization**
```python
# Use async/await consistently
# Already implemented in services
```

### Frontend Optimizations

1. **Code Splitting**
```typescript
// Use React.lazy for route-based splitting
const Dashboard = React.lazy(() => import('./Dashboard'));
```

2. **Asset Optimization**
```bash
# Vite automatically optimizes
npm run build
```

---

## 🧪 Testing Before Deployment

### Automated Tests

```bash
# Backend tests
cd backend
pytest --cov=. --cov-report=html

# Frontend tests
cd frontend
npm test

# Integration tests
# Test API endpoints
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","type":"sales","capabilities":[]}'
```

### Load Testing

```bash
# Install Apache Bench
# On Ubuntu: sudo apt-get install apache2-utils

# Test API endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Or use k6
k6 run load-test.js
```

---

## 📦 Final Submission Preparation

### 1. Code Repository

```bash
# Ensure all code is committed
git add .
git commit -m "Final submission - Nexus AI OS"
git push origin main

# Create release tag
git tag -a v1.0.0 -m "Hackathon submission"
git push origin v1.0.0

# Repository should include:
# - All source code
# - README.md
# - SETUP.md
# - PRESENTATION.md
# - PROJECT_SUMMARY.md
# - DEPLOYMENT.md (this file)
# - .env.example
# - docker-compose.yml
```

### 2. Demo Video

```bash
# Record 3-minute demo showing:
# 1. Self-organizing agent swarm (0:00-1:00)
# 2. Time Travel decision history (1:00-2:00)
# 3. Proactive risk prevention (2:00-3:00)

# Tools:
# - OBS Studio (free)
# - Loom (easy)
# - QuickTime (Mac)

# Upload to:
# - YouTube (unlisted)
# - Vimeo
# - Google Drive
```

### 3. Live Demo URLs

```bash
# Document all URLs:
# - Backend API: https://your-backend.railway.app
# - API Docs: https://your-backend.railway.app/docs
# - Frontend: https://your-frontend.vercel.app (if deployed)
# - GitHub: https://github.com/yourusername/nexus-ai-os
# - Demo Video: https://youtube.com/watch?v=...
```

### 4. Presentation Slides

```bash
# Create slides covering:
# 1. Problem ($50B market)
# 2. Solution (Neural Mesh)
# 3. Demo (live or video)
# 4. Technical architecture
# 5. Business value
# 6. Roadmap

# Tools:
# - Google Slides
# - PowerPoint
# - Canva
# - Pitch.com
```

### 5. Submission Checklist

- [ ] GitHub repository public and complete
- [ ] README.md with clear instructions
- [ ] All documentation files included
- [ ] .env.example with all variables
- [ ] Demo video recorded and uploaded
- [ ] Presentation slides created
- [ ] Backend deployed and accessible
- [ ] API documentation accessible
- [ ] Health check endpoint working
- [ ] Test agent creation working
- [ ] Test task execution working
- [ ] All URLs documented
- [ ] Submission form completed

---

## 🆘 Troubleshooting Deployment

### Common Issues

**1. Database Connection Errors**
```bash
# Check connection string format
# PostgreSQL: postgresql://user:pass@host:5432/dbname
# Redis: redis://host:6379

# Test connection
psql $DATABASE_URL
redis-cli -u $REDIS_URL ping
```

**2. CORS Errors**
```python
# Update CORS_ORIGINS in .env
CORS_ORIGINS=https://your-frontend.com,https://your-backend.com

# Or in main.py for development
allow_origins=["*"]  # Only for development!
```

**3. API Key Issues**
```bash
# Verify key is set
echo $GOOGLE_API_KEY

# Test key
curl https://generativelanguage.googleapis.com/v1/models \
  -H "x-goog-api-key: $GOOGLE_API_KEY"
```

**4. Memory Issues**
```bash
# Increase container memory
# In docker-compose.yml:
services:
  backend:
    mem_limit: 2g
    
# Or in cloud platform settings
```

**5. Timeout Issues**
```python
# Increase timeouts in config.py
AGENT_TIMEOUT = 600  # 10 minutes
MAX_TOKENS = 8192
```

---

## 📈 Post-Deployment Monitoring

### Key Metrics to Track

1. **API Performance**
   - Response time (< 2s for Flash, < 10s for Pro)
   - Error rate (< 1%)
   - Request rate

2. **Database Performance**
   - Connection pool usage
   - Query execution time
   - Cache hit rate

3. **Agent Performance**
   - Task completion rate
   - Average execution time
   - Success rate

4. **System Health**
   - CPU usage (< 80%)
   - Memory usage (< 80%)
   - Disk usage (< 80%)

### Monitoring Commands

```bash
# Check logs
docker-compose logs -f backend

# Check resource usage
docker stats

# Check database connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# Check Redis
redis-cli -u $REDIS_URL INFO stats
```

---

## 🎯 Success Criteria

### Deployment is Successful When:

- [ ] Health endpoint returns 200 OK
- [ ] API documentation loads at /docs
- [ ] Can create agent via API
- [ ] Can execute task via API
- [ ] Task returns result with agent coordination
- [ ] Knowledge graph stores relationships
- [ ] No errors in logs
- [ ] Response times within targets
- [ ] All databases connected
- [ ] Monitoring shows healthy metrics

---

## 📞 Support Resources

### Documentation
- **README.md**: Project overview
- **SETUP.md**: Local setup
- **PRESENTATION.md**: Hackathon strategy
- **PROJECT_SUMMARY.md**: Technical details
- **DEPLOYMENT.md**: This file

### External Resources
- **Google AI Studio**: https://ai.google.dev/
- **Railway Docs**: https://docs.railway.app/
- **Render Docs**: https://render.com/docs
- **Docker Docs**: https://docs.docker.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

## 🎉 Deployment Complete!

Once deployed, your Nexus AI OS will be:
- ✅ Accessible via public URL
- ✅ Running on production infrastructure
- ✅ Ready for hackathon demo
- ✅ Scalable and monitored
- ✅ Documented and maintainable

**Next**: Practice your presentation using PRESENTATION.md!

---

**Good luck with your hackathon submission! 🚀**