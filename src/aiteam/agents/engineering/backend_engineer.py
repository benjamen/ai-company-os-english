"""Backend Engineer Agent — Handles API design, databases, and infrastructure"""

from agents.base import run_claude_cli
from datetime import datetime


def run_backend_engineer_agent(workflow_id: str, feature_spec: str, tech_stack: str = "", security_context: str = "") -> dict:
    """
    Run the Backend Engineer agent.
    Input: feature specification and technical context
    Output: dict with API spec, database schema, and implementation guide
    """

    prompt = f"""You are an expert Backend Engineer specializing in API design and database architecture.

**Feature Specification:**
{feature_spec}

**Tech Stack:**
{tech_stack if tech_stack else "(To be determined)"}

**Security Context:**
{security_context if security_context else "(Standard OWASP Top 10 protection)"}

Please produce a comprehensive backend specification that includes:

1. **API Contract (OpenAPI 3.0)** — Complete endpoint specifications with request/response schemas
2. **Database Schema** — Tables, columns, relationships, indexes, constraints
3. **Data Models** — Validation rules, type definitions, transformations
4. **Authentication & Authorization** — Security requirements, permission model
5. **Error Handling** — Error codes, error messages, edge cases
6. **Performance Strategy** — Caching, query optimization, scalability considerations
7. **Observability** — Logging, tracing, metrics, monitoring points
8. **Infrastructure** — Deployment considerations, environment variables, secrets management
9. **Testing Strategy** — Unit tests, integration tests, performance tests
10. **Migration Plan** — If changing existing APIs, how to handle backwards compatibility

Format as markdown with embedded YAML for OpenAPI spec and SQL for schema.

IMPORTANT: Publish OpenAPI spec as a clear contract that Frontend can use immediately."""

    backend_content = run_claude_cli(prompt, timeout=180)

    return {
        "workflow_id": workflow_id,
        "agent_name": "backend_engineer",
        "output_type": "backend_spec",
        "content": backend_content,
        "model_used": "claude-cli",
        "timestamp": datetime.utcnow().isoformat()
    }


def run_backend_review_agent(workflow_id: str, backend_code: str, api_contract: str = "", performance_baseline: str = "") -> dict:
    """
    Run Backend Engineer as code reviewer.
    Validates backend code for security, performance, and API contract compliance.
    """

    prompt = f"""You are an expert Backend Code Reviewer specializing in API design and database patterns.

**Code to Review:**
{backend_code}

**API Contract:**
{api_contract if api_contract else "(Review against OpenAPI spec)"}

**Performance Baseline:**
{performance_baseline if performance_baseline else "(Standard < 200ms p95 response time)"}

Please perform a comprehensive code review covering:

1. **API Compliance** — Matches OpenAPI contract, proper status codes, consistent error handling
2. **Security** — Input validation, SQL injection prevention, authentication/authorization checks
3. **Database Design** — Query efficiency, N+1 problems, proper indexing, transaction handling
4. **Performance** — Response time, database query optimization, caching strategies
5. **Error Handling** — Proper error codes, meaningful error messages, logging
6. **Code Quality** — Patterns, maintainability, testability, documentation
7. **Deployment Safety** — Migrations, backwards compatibility, rollback strategy

Format as:
- ✅ **Passes**: [list of things done well]
- 🔒 **Security**: [security considerations and issues]
- ⚡ **Performance**: [performance analysis and optimizations]
- ⚠️ **Issues**: [list with severity: Critical/High/Medium/Low]
- 🔧 **Recommendations**: [suggested improvements]"""

    review_content = run_claude_cli(prompt, timeout=180)

    return {
        "workflow_id": workflow_id,
        "agent_name": "backend_engineer",
        "output_type": "backend_review",
        "content": review_content,
        "model_used": "claude-cli",
        "timestamp": datetime.utcnow().isoformat()
    }
