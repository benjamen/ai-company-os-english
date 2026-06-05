# Engineering Team Setup Guide

## ✅ What's Been Done

### 1. **Forked Reference Repository**
- Cloned `https://github.com/CronusL-1141/AI-company` to `/home/ben/ai-company-english`
- Updated CLAUDE.md to English
- Repository already has i18n support (defaults to English)

### 2. **Engineering Team Agents Created**
Three specialized agents ready to use:

```
src/aiteam/agents/engineering/
├── backend_engineer.py        # API & database design
├── frontend_engineer.py        # UI/component development
├── qa_specialist_agent.py      # Testing & quality validation
└── team_orchestrator.py        # Manages collaboration workflow
```

### 3. **Key Features**
- **Contract-First Development** — Backend publishes API specs before implementation
- **Parallel Workflows** — Frontend and Backend develop simultaneously
- **Quality Gates** — QA sign-off required before release
- **Collaboration Model** — Clear handoffs and dependencies between agents

---

## 📋 Remaining Integration Tasks

### Task 1: Add Engineering Team API Endpoints
**Location**: `src/aiteam/api/` or equivalent FastAPI router

Add endpoints:
```python
POST   /api/engineering-team/start-feature
GET    /api/engineering-team/members
GET    /api/engineering-team/{workflow_id}/status
POST   /api/engineering-team/{workflow_id}/plan-frontend
POST   /api/engineering-team/{workflow_id}/plan-qa
```

### Task 2: Create Engineering Team Page in React Dashboard
**Location**: `dashboard/src/pages/EngineeringTeamPage.tsx`

Should display:
- Team members (Backend Engineer, Frontend Engineer, QA Specialist)
- Current workflows and their status
- Workflow phases and approval gates
- Quick actions to start new features

### Task 3: Add Team to Navigation
**Location**: `dashboard/src/components/layout/AppLayout.tsx`

Add menu item:
```
Engineering → Teams → Engineering Team
```

### Task 4: Register Team in Agent Config
**Location**: Agent registry/configuration

Register the three agents:
- `engineering.backend_engineer`
- `engineering.frontend_engineer`
- `engineering.qa_specialist`

---

## 🚀 Quick Start After Setup

### 1. **Start the Backend**
```bash
cd /home/ben/ai-company-english
python -m uvicorn src.aiteam.api.app:app --host 0.0.0.0 --port 8000 --reload
```

### 2. **Start the Dashboard**
```bash
cd /home/ben/ai-company-english/dashboard
npm install
npm run dev
```

Dashboard will be available at `http://localhost:5174/` (defaults to English)

### 3. **Test Engineering Team API**
```bash
curl http://localhost:8000/api/engineering-team/members
```

---

## 📚 Documentation Files

- **Team Structure**: `/home/ben/software_engineering_team.md`
- **Configuration**: `/home/ben/team_agent_config.yaml`
- **Collaboration Example**: `/home/ben/team_collaboration_example.md`

---

## 🎯 Workflow: How to Use the Engineering Team

### Step 1: Start Feature Development
```bash
curl -X POST http://localhost:8000/api/engineering-team/start-feature \
  -H "Content-Type: application/json" \
  -d '{
    "feature_spec": "User preferences page with theme/language/notification settings",
    "repo_tech_stack": "React + FastAPI + SQLite",
    "jira_key": "PROJ-123"
  }'
```

### Step 2: Backend Engineer Designs API
- Returns OpenAPI specification
- Sets up database schema
- Creates mock server

### Step 3: Frontend & QA Plan in Parallel
- Frontend Engineer creates component architecture
- QA Specialist creates test strategy

### Step 4: All Develop in Parallel
- Backend implements APIs
- Frontend builds components
- QA prepares test environment

### Step 5: Code Review Gates
- Frontend reviews Backend API adherence
- Backend reviews Frontend integration
- QA reviews test coverage

### Step 6: QA Testing & Validation
- Automated tests (unit, integration, E2E)
- Performance testing
- Accessibility validation

### Step 7: Release Sign-Off
- QA Specialist approves or requests fixes
- Feature released to production

---

## 🔧 File Structure Reference

```
ai-company-english/
├── src/aiteam/
│   ├── agents/engineering/
│   │   ├── backend_engineer.py          ✅ NEW
│   │   ├── frontend_engineer.py         ✅ NEW
│   │   ├── qa_specialist_agent.py       ✅ NEW
│   │   └── team_orchestrator.py         ✅ NEW
│   ├── api/
│   │   └── [Add engineering team endpoints here]
│   └── types.py
├── dashboard/
│   ├── src/
│   │   ├── pages/
│   │   │   └── [Create EngineeringTeamPage.tsx here]
│   │   └── i18n/
│   │       ├── en.ts                    (already English)
│   │       └── zh.ts
│   └── vite.config.ts
└── CLAUDE.md                             ✅ UPDATED
```

---

## 🌐 Language Settings

The dashboard automatically detects user browser language:
- Chinese browser → 中文
- English/other → English (default)

Override via language selector in settings.

---

## ⚡ Next Steps

1. **Backend Integration** (2-3 hours)
   - Create FastAPI routers for engineering team endpoints
   - Wire up orchestrator to main app
   - Test API endpoints

2. **Dashboard Integration** (3-4 hours)
   - Create EngineeringTeamPage component
   - Add to navigation and routes
   - Connect to backend APIs
   - Style to match existing dashboard

3. **Testing** (1-2 hours)
   - Test complete workflow end-to-end
   - Verify all three agents activate correctly
   - Test approval gates

4. **Documentation** (1 hour)
   - Update README with engineering team features
   - Create user guide for team workflow

**Total Time**: ~7-10 hours for full implementation

---

## 📞 Support

Reference documentation:
- Architecture: See `docs/architecture.md` in the repo
- API Patterns: Check existing endpoints in `src/aiteam/api/`
- Component Examples: Look at other pages in `dashboard/src/pages/`
- i18n: See `dashboard/src/i18n/` for translation pattern

---

## 🎯 Success Criteria

✅ All three engineering agents registered and callable
✅ Engineering Team dashboard page displays all agents
✅ Can start a feature workflow via UI
✅ All endpoints tested and working
✅ UI fully in English
✅ Documentation complete

