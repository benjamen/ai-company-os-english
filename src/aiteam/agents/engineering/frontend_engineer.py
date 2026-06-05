"""Frontend Engineer Agent — Handles UI/component design and implementation"""

from agents.base import run_claude_cli
from datetime import datetime


def run_frontend_engineer_agent(workflow_id: str, feature_spec: str, api_spec: str = "", design_system: str = "") -> dict:
    """
    Run the Frontend Engineer agent.
    Input: feature specification and API specification from Backend Engineer
    Output: dict with frontend implementation plan, components, and test hooks
    """

    prompt = f"""You are an expert Frontend Engineer specializing in modern web development with React/Vue/Angular.

**Feature Specification:**
{feature_spec}

**API Specification (from Backend Engineer):**
{api_spec if api_spec else "(API spec not yet available)"}

**Design System Guidelines:**
{design_system if design_system else "(Design system not specified)"}

Please produce a comprehensive frontend implementation guide that includes:

1. **Component Architecture** — Proposed component structure, hierarchy, reusability
2. **State Management** — How to handle state (Redux, Context, Vuex, etc.)
3. **API Integration** — How to integrate with backend endpoints, error handling, loading states
4. **Accessibility (a11y)** — WCAG 2.1 AA compliance requirements, ARIA labels, semantic HTML
5. **Performance Optimization** — Code splitting, lazy loading, image optimization, Core Web Vitals targets
6. **User Experience** — Loading states, error messages, offline handling, responsive design
7. **Test Hooks** — Specific attributes/IDs needed for automated testing
8. **Component Checklist** — Detailed checklist of components to build
9. **Implementation Order** — Suggested order of implementation
10. **Browser Compatibility** — Target browsers and fallback strategies

Format as markdown with clear sections. Include component mockups in ASCII if helpful.

IMPORTANT: Flag any API design issues or missing specifications that would block implementation."""

    frontend_content = run_claude_cli(prompt, timeout=180)

    return {
        "workflow_id": workflow_id,
        "agent_name": "frontend_engineer",
        "output_type": "frontend_plan",
        "content": frontend_content,
        "model_used": "claude-cli",
        "timestamp": datetime.utcnow().isoformat()
    }


def run_frontend_review_agent(workflow_id: str, frontend_code: str, accessibility_requirements: str = "", performance_baseline: str = "") -> dict:
    """
    Run Frontend Engineer as code reviewer.
    Validates frontend code for patterns, accessibility, performance, and testability.
    """

    prompt = f"""You are an expert Frontend Code Reviewer specializing in React/Vue best practices.

**Code to Review:**
{frontend_code}

**Accessibility Requirements:**
{accessibility_requirements if accessibility_requirements else "(Standard WCAG 2.1 AA)"}

**Performance Baseline:**
{performance_baseline if performance_baseline else "(Standard Core Web Vitals)"}

Please perform a comprehensive code review covering:

1. **Code Quality** — Patterns, reusability, maintainability
2. **Accessibility** — WCAG 2.1 AA compliance, ARIA usage, semantic HTML
3. **Performance** — Bundle size, render performance, Core Web Vitals impact
4. **Testing** — Test coverage, test hooks, component testability
5. **Browser Compatibility** — Cross-browser issues, polyfills needed
6. **Best Practices** — Framework patterns, anti-patterns, recommendations

Format as:
- ✅ **Passes**: [list of things done well]
- ⚠️ **Issues**: [list with severity levels: Critical/High/Medium/Low]
- 🔧 **Recommendations**: [suggested improvements]

Be constructive and educational in feedback."""

    review_content = run_claude_cli(prompt, timeout=180)

    return {
        "workflow_id": workflow_id,
        "agent_name": "frontend_engineer",
        "output_type": "frontend_review",
        "content": review_content,
        "model_used": "claude-cli",
        "timestamp": datetime.utcnow().isoformat()
    }
