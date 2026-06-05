"""QA Specialist Agent — Handles testing strategy, quality validation, and release sign-off"""

from agents.base import run_claude_cli
from datetime import datetime


def run_qa_specialist_agent(workflow_id: str, feature_spec: str, api_spec: str = "", acceptance_criteria: str = "") -> dict:
    """
    Run the QA Specialist agent.
    Input: feature specification and acceptance criteria
    Output: dict with test strategy, test cases, and quality metrics
    """

    prompt = f"""You are an expert QA Specialist with expertise in test automation and quality strategy.

**Feature Specification:**
{feature_spec}

**API Specification:**
{api_spec if api_spec else "(API spec not yet available)"}

**Acceptance Criteria:**
{acceptance_criteria if acceptance_criteria else "(From feature requirements)"}

Please produce a comprehensive test strategy document that includes:

1. **Test Strategy** — Overall approach, coverage targets (≥80% code, 100% critical paths)
2. **Test Categories** — Unit tests, integration tests, E2E tests, performance tests, accessibility tests
3. **Test Plan** — Detailed test cases with:
   - Test ID and description
   - Pre-conditions and post-conditions
   - Test steps and expected results
   - Data requirements
   - Pass/fail criteria

4. **Test Data** — Fixtures, factories, seed data, edge cases
5. **Performance Testing** — Baselines, load test scenarios, acceptable thresholds
6. **Accessibility Testing** — WCAG 2.1 AA checklist, screen reader testing, keyboard navigation
7. **Security Testing** — OWASP considerations, input validation, permission boundaries
8. **Automation Plan** — Which tests should be automated, framework recommendations
9. **Test Environment** — Setup requirements, dependencies, mocking strategy
10. **Defect Management** — Severity levels, SLA targets, defect triage process

Format as markdown with clear sections and detailed checklists.

IMPORTANT: Include specific test cases that validate the acceptance criteria."""

    qa_content = run_claude_cli(prompt, timeout=180)

    return {
        "workflow_id": workflow_id,
        "agent_name": "qa_specialist",
        "output_type": "qa_test_plan",
        "content": qa_content,
        "model_used": "claude-cli",
        "timestamp": datetime.utcnow().isoformat()
    }


def run_qa_validation_agent(workflow_id: str, test_results: str, quality_metrics: str = "", defect_log: str = "") -> dict:
    """
    Run QA Specialist as validator.
    Analyzes test results and determines if feature is ready for release.
    """

    prompt = f"""You are an expert QA Validator responsible for release sign-off decisions.

**Test Results:**
{test_results}

**Quality Metrics:**
{quality_metrics if quality_metrics else "(Standard: ≥80% coverage, 0 critical defects, < 2% escape rate)"}

**Defect Log:**
{defect_log if defect_log else "(No defects reported)"}

Please analyze and provide:

1. **Test Coverage Analysis** — What was tested, coverage percentages, gaps
2. **Quality Assessment** — How well does this meet quality standards?
3. **Risk Assessment** — Remaining risks, edge cases not covered, potential issues
4. **Defect Status** — Summary of defects found, severity distribution, resolution status
5. **Performance Validation** — API response times, database performance, core web vitals
6. **Accessibility Validation** — WCAG 2.1 AA compliance status
7. **Release Readiness** — Is this ready for production?

Output format:
- 🟢 **READY**: List of go criteria met
- 🟡 **CONDITIONAL**: Minor issues with workarounds
- 🔴 **BLOCKED**: Critical issues preventing release

End with clear recommendation: **APPROVED FOR RELEASE**, **CONDITIONAL APPROVAL**, or **REJECT**."""

    validation_content = run_claude_cli(prompt, timeout=180)

    return {
        "workflow_id": workflow_id,
        "agent_name": "qa_specialist",
        "output_type": "qa_validation",
        "content": validation_content,
        "model_used": "claude-cli",
        "timestamp": datetime.utcnow().isoformat()
    }
