# Nexus AI OS - Complete Setup Guide

This guide will walk you through setting up Nexus AI Operating System from scratch.

## Prerequisites

### Required Software
- **Docker Desktop** (v24.0+) - [Download](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Google AI API Key** - [Get Free Key](https://ai.google.dev/)

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 10GB free space
- **CPU**: 4 cores recommended

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nexus-ai-os.git
cd nexus-ai-os
```

### 2. Get Google AI API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Sign in with your Google account
4. Create a new API key
5. Copy the key (you'll need it in the next step)

**Note**: The free tier includes generous limits perfect for development and hackathon demos.

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

**Required Configuration**:
```bash
# Add your Google AI API key
GOOGLE_API_KEY=your_actual_api_key_here

# Other settings can use defaults for local development
```

### 4. Start the Services

```bash
# Start all services in detached mode
docker-compose up -d

# This will start:
# - PostgreSQL (port 5432)
# - Redis (port 6379)
# - Neo4j (ports 7474, 7687)
# - Qdrant (port 6333)
# - Backend API (port 8000)
# - Frontend (port 3000)
# - Celery Worker
```

### 5. Wait for Services to Initialize

```bash
# Watch the logs to see when everything is ready
docker-compose logs -f backend

# Look for this message:
# "Nexus AI OS v1.0.0 started"
# "API documentation: http://localhost:8000/docs"

# Press Ctrl+C to stop watching logs
```

**Typical startup time**: 30-60 seconds

### 6. Verify Installation

#### Check Service Health

```bash
# Check all services are running
docker-compose ps

# All services should show "Up" status
```

#### Test Backend API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0","environment":"development"}
```

#### Access Web Interfaces

1. **Frontend Dashboard**: http://localhost:3000
2. **API Documentation**: http://localhost:8000/docs
3. **Neo4j Browser**: http://localhost:7474
   - Username: `neo4j`
   - Password: `nexus_graph_password`

### 7. Create Your First Agent

#### Using the API

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales Assistant",
    "type": "sales",
    "description": "Analyzes sales data and provides insights",
    "capabilities": ["data_analysis", "forecasting", "customer_insights"],
    "configuration": {},
    "metadata": {
      "department": "Sales",
      "region": "North America"
    }
  }'
```

#### Using the Web Interface

1. Go to http://localhost:3000
2. Click "Create Agent"
3. Fill in the form
4. Click "Create"

### 8. Run Your First Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "demo_task_001",
    "agent_id": "auto",
    "task_type": "analysis",
    "description": "Analyze Q4 2024 sales performance and identify top 3 trends",
    "priority": 8,
    "context": {
      "quarter": "Q4",
      "year": 2024,
      "focus_areas": ["revenue", "customer_acquisition", "product_performance"]
    },
    "timeout": 300
  }'
```

The system will:
1. Analyze the task requirements
2. Route it to the best-suited agent
3. Execute using Gemini AI
4. Store results in the knowledge graph
5. Return the completed result

## Troubleshooting

### Services Won't Start

**Problem**: Docker containers fail to start

**Solutions**:
```bash
# Check Docker is running
docker --version

# Check available disk space
df -h  # Linux/Mac
# On Windows: Check in File Explorer

# Restart Docker Desktop
# Then try again:
docker-compose down
docker-compose up -d
```

### Port Already in Use

**Problem**: Error like "port 8000 is already allocated"

**Solutions**:
```bash
# Find what's using the port (example for port 8000)
# On Windows:
netstat -ano | findstr :8000

# On Mac/Linux:
lsof -i :8000

# Kill the process or change the port in docker-compose.yml
```

### Google API Key Not Working

**Problem**: "Invalid API key" or "Authentication failed"

**Solutions**:
1. Verify the key is correct in `.env`
2. Check there are no extra spaces or quotes
3. Ensure the key is enabled in Google AI Studio
4. Try generating a new key

**Correct format in .env**:
```bash
GOOGLE_API_KEY=AIzaSyD...your_key_here...xyz123
```

### Database Connection Errors

**Problem**: "Could not connect to database"

**Solutions**:
```bash
# Check database containers are running
docker-compose ps

# Restart specific service
docker-compose restart postgres
docker-compose restart neo4j

# Check logs for specific service
docker-compose logs postgres
docker-compose logs neo4j
```

### Frontend Not Loading

**Problem**: http://localhost:3000 shows error

**Solutions**:
```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend

# If still not working, rebuild
docker-compose up -d --build frontend
```

## Development Mode

### Running Backend Locally (Without Docker)

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

# Start databases only
docker-compose up -d postgres redis neo4j qdrant

# Run backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Frontend Locally (Without Docker)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will be available at http://localhost:5173
```

## Stopping the Services

```bash
# Stop all services
docker-compose down

# Stop and remove all data (WARNING: This deletes all data!)
docker-compose down -v
```

## Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

## Performance Optimization

### For Development

```bash
# Allocate more resources to Docker Desktop
# Settings > Resources > Advanced
# Recommended: 4 CPUs, 8GB RAM
```

### For Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guide.

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Create Multiple Agents**: Try different agent types
3. **Test Collaboration**: Create tasks that require multiple agents
4. **View Knowledge Graph**: Check Neo4j browser to see relationships
5. **Monitor Performance**: Watch agent metrics in the dashboard

## Getting Help

- **Documentation**: Check README.md for detailed information
- **API Reference**: http://localhost:8000/docs
- **Issues**: Create an issue on GitHub
- **Discord**: Join our community for real-time help

## Common Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart [service_name]

# Rebuild a service
docker-compose up -d --build [service_name]

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats
```

## Success Checklist

- [ ] Docker Desktop installed and running
- [ ] Repository cloned
- [ ] Google API key obtained and configured
- [ ] All services started successfully
- [ ] Health check passes
- [ ] Frontend accessible at http://localhost:3000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] First agent created successfully
- [ ] First task executed successfully
- [ ] Knowledge graph visible in Neo4j browser

---

**Congratulations!** 🎉 You now have Nexus AI OS running locally!

For questions or issues, please check the troubleshooting section or reach out to the community.