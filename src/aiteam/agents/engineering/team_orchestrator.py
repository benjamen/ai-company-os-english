"""Engineering Team Orchestrator — Manages three-agent collaboration workflow"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from agents.engineering.backend_engineer import run_backend_engineer_agent
from agents.engineering.frontend_engineer import run_frontend_engineer_agent
from agents.engineering.qa_specialist_agent import run_qa_specialist_agent, run_qa_validation_agent


class EngineeringTeam:
    """Orchestrates collaboration between Frontend, Backend, and QA agents"""

    def __init__(self):
        self.team_members = {
            "backend_engineer": {
                "name": "Backend Engineer",
                "role": "API & Database Design",
                "tier": 2,
                "status": "ready"
            },
            "frontend_engineer": {
                "name": "Frontend Engineer",
                "role": "UI/Component Implementation",
                "tier": 2,
                "status": "ready"
            },
            "qa_specialist": {
                "name": "QA Specialist",
                "role": "Testing & Quality",
                "tier": 2,
                "status": "ready"
            }
        }
        self.active_workflows = {}

    def start_feature_workflow(self, feature_spec: str, repo_tech_stack: str = "", jira_key: str = "") -> Dict:
        """
        Initiate a feature workflow with the engineering team.
        Returns workflow ID and initial collaboration plan.
        """
        workflow_id = f"eng-{uuid.uuid4().hex[:8]}"
        workflow_started = datetime.utcnow().isoformat()

        workflow = {
            "id": workflow_id,
            "jira_key": jira_key,
            "feature_spec": feature_spec,
            "tech_stack": repo_tech_stack,
            "started_at": workflow_started,
            "status": "in_progress",
            "phases": {
                "design": {"status": "in_progress", "owner": "backend_engineer"},
                "frontend_planning": {"status": "pending", "owner": "frontend_engineer"},
                "qa_planning": {"status": "pending", "owner": "qa_specialist"},
                "development": {"status": "pending"},
                "review": {"status": "pending"},
                "qa_testing": {"status": "pending", "owner": "qa_specialist"},
                "release": {"status": "pending"}
            },
            "artifacts": {},
            "gates": {
                "api_contract_ready": {"status": "pending", "required_by": "backend_engineer"},
                "frontend_ready": {"status": "pending", "required_by": "frontend_engineer"},
                "qa_signoff": {"status": "pending", "required_by": "qa_specialist"}
            }
        }

        self.active_workflows[workflow_id] = workflow

        # Phase 1: Backend designs API spec
        backend_output = run_backend_engineer_agent(
            workflow_id=workflow_id,
            feature_spec=feature_spec,
            tech_stack=repo_tech_stack
        )

        workflow["artifacts"]["api_spec"] = backend_output
        workflow["phases"]["design"]["status"] = "complete"
        workflow["gates"]["api_contract_ready"]["status"] = "ready_for_review"

        return {
            "workflow_id": workflow_id,
            "status": "api_spec_ready",
            "next_steps": [
                "Frontend Engineer reviews API spec and creates component plan",
                "QA Specialist creates test strategy",
                "Then Backend & Frontend develop in parallel"
            ],
            "backend_output": backend_output
        }

    def plan_frontend_work(self, workflow_id: str) -> Dict:
        """Frontend Engineer creates implementation plan based on API spec"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}

        workflow = self.active_workflows[workflow_id]
        api_spec = workflow["artifacts"].get("api_spec", {}).get("content", "")

        frontend_output = run_frontend_engineer_agent(
            workflow_id=workflow_id,
            feature_spec=workflow["feature_spec"],
            api_spec=api_spec,
            design_system=workflow.get("design_system", "")
        )

        workflow["artifacts"]["frontend_plan"] = frontend_output
        workflow["phases"]["frontend_planning"]["status"] = "complete"

        return {
            "status": "frontend_plan_ready",
            "frontend_output": frontend_output
        }

    def plan_qa_work(self, workflow_id: str) -> Dict:
        """QA Specialist creates test strategy"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}

        workflow = self.active_workflows[workflow_id]
        api_spec = workflow["artifacts"].get("api_spec", {}).get("content", "")
        acceptance_criteria = workflow.get("acceptance_criteria", "")

        qa_output = run_qa_specialist_agent(
            workflow_id=workflow_id,
            feature_spec=workflow["feature_spec"],
            api_spec=api_spec,
            acceptance_criteria=acceptance_criteria
        )

        workflow["artifacts"]["qa_plan"] = qa_output
        workflow["phases"]["qa_planning"]["status"] = "complete"

        return {
            "status": "qa_plan_ready",
            "qa_output": qa_output
        }

    def request_frontend_review(self, workflow_id: str, frontend_code: str) -> Dict:
        """Request Frontend Engineer to review code"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}

        workflow = self.active_workflows[workflow_id]
        from agents.engineering.frontend_engineer import run_frontend_review_agent

        review = run_frontend_review_agent(
            workflow_id=workflow_id,
            frontend_code=frontend_code,
            accessibility_requirements="WCAG 2.1 AA",
            performance_baseline="Core Web Vitals green"
        )

        workflow["artifacts"]["frontend_review"] = review

        return {
            "status": "frontend_review_complete",
            "review": review
        }

    def request_backend_review(self, workflow_id: str, backend_code: str) -> Dict:
        """Request Backend Engineer to review code"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}

        workflow = self.active_workflows[workflow_id]
        from agents.engineering.backend_engineer import run_backend_review_agent

        review = run_backend_review_agent(
            workflow_id=workflow_id,
            backend_code=backend_code,
            api_contract=workflow["artifacts"].get("api_spec", {}).get("content", ""),
            performance_baseline="< 100ms p95"
        )

        workflow["artifacts"]["backend_review"] = review

        return {
            "status": "backend_review_complete",
            "review": review
        }

    def validate_for_qa(self, workflow_id: str, test_results: str, quality_metrics: str = "") -> Dict:
        """QA Specialist validates and signs off on release readiness"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}

        workflow = self.active_workflows[workflow_id]

        validation = run_qa_validation_agent(
            workflow_id=workflow_id,
            test_results=test_results,
            quality_metrics=quality_metrics
        )

        workflow["artifacts"]["qa_validation"] = validation
        workflow["phases"]["qa_testing"]["status"] = "complete"

        # Extract recommendation
        if "APPROVED FOR RELEASE" in validation.get("content", ""):
            workflow["gates"]["qa_signoff"]["status"] = "approved"
            workflow["status"] = "ready_for_release"
        else:
            workflow["gates"]["qa_signoff"]["status"] = "needs_work"
            workflow["status"] = "blocked"

        return {
            "status": workflow["status"],
            "validation": validation,
            "can_release": workflow["gates"]["qa_signoff"]["status"] == "approved"
        }

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get current status of a workflow"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}

        workflow = self.active_workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "phases": workflow["phases"],
            "gates": workflow["gates"],
            "artifacts_summary": {
                key: {"type": val.get("output_type", "unknown")}
                for key, val in workflow["artifacts"].items()
            }
        }

    def list_team_members(self) -> Dict:
        """List all team members and their current status"""
        return {
            "team": "Engineering Team",
            "members": self.team_members,
            "total_capacity": len(self.team_members),
            "available_members": len([m for m in self.team_members.values() if m["status"] == "ready"])
        }

    def get_collaboration_flow(self) -> Dict:
        """Return the standard collaboration workflow"""
        return {
            "workflow_name": "Feature Development with Engineering Team",
            "phases": [
                {
                    "phase": "Design",
                    "owner": "Backend Engineer",
                    "deliverables": ["API Specification (OpenAPI)", "Database Schema", "Implementation Plan"],
                    "duration": "1-2 days"
                },
                {
                    "phase": "Planning",
                    "owner": "Frontend Engineer & QA Specialist",
                    "deliverables": ["Component Architecture", "Test Strategy", "Test Cases"],
                    "duration": "1 day",
                    "parallel": True
                },
                {
                    "phase": "Development",
                    "owner": "Frontend Engineer & Backend Engineer",
                    "deliverables": ["Frontend Components", "Backend APIs"],
                    "duration": "2-5 days",
                    "parallel": True,
                    "dependencies": ["API Specification"]
                },
                {
                    "phase": "Code Review",
                    "owner": "All team members",
                    "deliverables": ["Code Review Comments", "Approval"],
                    "duration": "1 day"
                },
                {
                    "phase": "QA Testing",
                    "owner": "QA Specialist",
                    "deliverables": ["Test Execution Report", "Defect List"],
                    "duration": "2-3 days"
                },
                {
                    "phase": "Defect Resolution",
                    "owner": "Frontend Engineer & Backend Engineer",
                    "deliverables": ["Fixed Code", "Regression Tests"],
                    "duration": "1-2 days"
                },
                {
                    "phase": "Release",
                    "owner": "QA Specialist",
                    "deliverables": ["QA Sign-off", "Release Notes"],
                    "duration": "0.5 days"
                }
            ],
            "total_timeline": "7-14 days",
            "gates": [
                {"gate": "API Contract", "owner": "Backend", "blocks": "Frontend"},
                {"gate": "Code Review", "owner": "All", "blocks": "QA Testing"},
                {"gate": "QA Sign-off", "owner": "QA", "blocks": "Release"}
            ]
        }


# Global team instance
engineering_team = EngineeringTeam()
