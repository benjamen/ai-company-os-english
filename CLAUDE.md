# AI Company OS - Engineering Edition

**Tech Stack**: Python 3.12 + FastAPI | React 19 + Vite | SQLite
**Architecture**: Storage → API → Dashboard (see docs/architecture.md)

## Core Constraints
- All outputs use English
- Shared types only reference `src/aiteam/types.py`
- Code style: PEP 8, type annotations, async-first

## Engineering Team Integration
- **Backend Engineer Agent** — API design, database architecture, security
- **Frontend Engineer Agent** — UI components, accessibility, performance
- **QA Specialist Agent** — Testing strategy, quality validation, release sign-off

## Leader Core Behaviors
- Focus on coordination and delegation to team members
- New requirements go on the task board first
- System-level features start with design documents
- Complete rules auto-injected via SessionStart, also queryable at GET /api/system/rules

