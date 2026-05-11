#!/bin/bash

# Nexus AI OS - Deployment Verification Script
# This script tests all critical functionality before hackathon submission

set -e  # Exit on error

echo "🚀 Nexus AI OS - Deployment Verification"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
API_URL="${API_URL:-http://localhost:8000}"
TIMEOUT=30

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((TESTS_PASSED++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((TESTS_FAILED++))
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Test 1: Health Check
echo "Test 1: Health Check Endpoint"
echo "------------------------------"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/health" || echo "000")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    print_success "Health endpoint returned 200 OK"
    echo "Response: $RESPONSE_BODY"
else
    print_error "Health endpoint failed (HTTP $HTTP_CODE)"
fi
echo ""

# Test 2: API Documentation
echo "Test 2: API Documentation"
echo "-------------------------"
DOCS_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/docs" || echo "000")
HTTP_CODE=$(echo "$DOCS_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    print_success "API documentation accessible at $API_URL/docs"
else
    print_error "API documentation not accessible (HTTP $HTTP_CODE)"
fi
echo ""

# Test 3: Create Agent
echo "Test 3: Create Agent"
echo "--------------------"
AGENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/agents" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Test Agent",
        "type": "sales",
        "description": "Automated test agent",
        "capabilities": ["testing", "verification"],
        "configuration": {},
        "metadata": {"test": true}
    }' || echo '{"error":"request failed"}\n000')

HTTP_CODE=$(echo "$AGENT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$AGENT_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "201" ]; then
    AGENT_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    print_success "Agent created successfully (ID: $AGENT_ID)"
    echo "Response: $RESPONSE_BODY"
else
    print_error "Agent creation failed (HTTP $HTTP_CODE)"
    echo "Response: $RESPONSE_BODY"
    AGENT_ID=""
fi
echo ""

# Test 4: List Agents
echo "Test 4: List Agents"
echo "-------------------"
LIST_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/agents" || echo "000")
HTTP_CODE=$(echo "$LIST_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$LIST_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    AGENT_COUNT=$(echo "$RESPONSE_BODY" | grep -o '"id"' | wc -l)
    print_success "Listed agents successfully (Count: $AGENT_COUNT)"
else
    print_error "List agents failed (HTTP $HTTP_CODE)"
fi
echo ""

# Test 5: Get Agent Details
if [ -n "$AGENT_ID" ]; then
    echo "Test 5: Get Agent Details"
    echo "-------------------------"
    GET_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/agents/$AGENT_ID" || echo "000")
    HTTP_CODE=$(echo "$GET_RESPONSE" | tail -n1)
    
    if [ "$HTTP_CODE" = "200" ]; then
        print_success "Retrieved agent details successfully"
    else
        print_error "Get agent details failed (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 6: Create Task
echo "Test 6: Create and Execute Task"
echo "--------------------------------"
TASK_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/tasks" \
    -H "Content-Type: application/json" \
    -d '{
        "task_id": "test_task_001",
        "agent_id": "auto",
        "task_type": "test",
        "description": "Automated test task for verification",
        "priority": 5,
        "context": {"test": true},
        "timeout": 60
    }' || echo '{"error":"request failed"}\n000')

HTTP_CODE=$(echo "$TASK_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$TASK_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    print_success "Task created and executed successfully"
    echo "Response: $RESPONSE_BODY"
else
    print_error "Task execution failed (HTTP $HTTP_CODE)"
    echo "Response: $RESPONSE_BODY"
fi
echo ""

# Test 7: Knowledge Graph Stats
echo "Test 7: Knowledge Graph Statistics"
echo "-----------------------------------"
STATS_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/knowledge/stats" || echo "000")
HTTP_CODE=$(echo "$STATS_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$STATS_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    print_success "Knowledge graph stats retrieved successfully"
    echo "Response: $RESPONSE_BODY"
else
    print_error "Knowledge graph stats failed (HTTP $HTTP_CODE)"
fi
echo ""

# Test 8: Agent Metrics
if [ -n "$AGENT_ID" ]; then
    echo "Test 8: Agent Performance Metrics"
    echo "----------------------------------"
    METRICS_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/agents/$AGENT_ID/metrics" || echo "000")
    HTTP_CODE=$(echo "$METRICS_RESPONSE" | tail -n1)
    
    if [ "$HTTP_CODE" = "200" ]; then
        print_success "Agent metrics retrieved successfully"
    else
        print_error "Agent metrics failed (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 9: WebSocket Connection (optional)
echo "Test 9: WebSocket Support"
echo "-------------------------"
print_info "WebSocket endpoint available at: ws://${API_URL#http://}/ws"
print_info "Manual testing recommended for WebSocket functionality"
echo ""

# Test 10: Database Connections
echo "Test 10: Database Connectivity"
echo "------------------------------"
print_info "Checking database connections..."

# Check if services are running (Docker)
if command -v docker-compose &> /dev/null; then
    POSTGRES_STATUS=$(docker-compose ps postgres 2>/dev/null | grep -c "Up" || echo "0")
    REDIS_STATUS=$(docker-compose ps redis 2>/dev/null | grep -c "Up" || echo "0")
    NEO4J_STATUS=$(docker-compose ps neo4j 2>/dev/null | grep -c "Up" || echo "0")
    QDRANT_STATUS=$(docker-compose ps qdrant 2>/dev/null | grep -c "Up" || echo "0")
    
    if [ "$POSTGRES_STATUS" = "1" ]; then
        print_success "PostgreSQL is running"
    else
        print_error "PostgreSQL is not running"
    fi
    
    if [ "$REDIS_STATUS" = "1" ]; then
        print_success "Redis is running"
    else
        print_error "Redis is not running"
    fi
    
    if [ "$NEO4J_STATUS" = "1" ]; then
        print_success "Neo4j is running"
    else
        print_error "Neo4j is not running"
    fi
    
    if [ "$QDRANT_STATUS" = "1" ]; then
        print_success "Qdrant is running"
    else
        print_error "Qdrant is not running"
    fi
else
    print_info "Docker Compose not available - skipping database checks"
fi
echo ""

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! System is ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please review the errors above.${NC}"
    exit 1
fi

# Made with Bob
