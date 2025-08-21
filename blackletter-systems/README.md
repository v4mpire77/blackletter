# Blackletter — Assurance-First Legal Tech Repo

This repository turns your strategic plan into a **clickable operating system**:
Goals → Epics → Issues → PRs → Releases → KPIs.

## What’s inside
- **GitHub Projects** templates (issue forms & labels) for Epics/Features/Bugs/Runbooks.
- **Workflows** enforcing Assurance: SLA timers, eval-based Assurance Cards, release notes, status page.
- **Docs** for Pricing & Metering, Evidence Chain, HITL guardrails.
- **Minimal app** (Node + TypeScript + Express) with a stubbed rules/evidence API and demo endpoints.
- **VS Code** config for a smooth start on Windows.

> Date scaffold generated: 2025-08-20

## Quick start (Windows PowerShell)
```powershell
# 1) Unzip then enter the folder
cd .\blackletter-github-project

# 2) Initialize git and create a new GitHub repo (or connect to an existing remote)
git init
git add .
git commit -m "chore: initial scaffold"
# Create a repo on GitHub then:
git remote add origin https://github.com/YOUR-USER/blackletter.git
git branch -M main
git push -u origin main

# 3) Install and run (requires Node 20+)
npm install
npm run dev
# Open http://localhost:3000/health
```

## VS Code
- Open the folder in VS Code (`File → Open Folder`).
- Recommended extensions will be suggested automatically.
- Debug config included: press **F5** to run the dev server.

## Where to click
- **Issues → New issue**: pick *Epic*, *Feature*, *Bug*, or *Runbook*.
- **Actions**: see *Assurance Eval*, *SLA Timer*, *Release Notes*, *Status Page* workflows.
- **Projects**: create a Project Board and add issues; use labels like `assurance`, `sla:10d`, `hitl`.

## Env (example)
Create `.env` with the following (customize as needed):
```
PORT=3000
ASSURANCE_SLA_DAYS=10
```

## License
Private repo by default. Add a LICENSE if you plan to open source.
