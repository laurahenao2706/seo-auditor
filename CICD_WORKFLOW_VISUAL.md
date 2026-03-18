# 🔄 CI/CD Workflow Visualization

## 📊 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TRIGGER EVENTS                            │
├─────────────────────────────────────────────────────────────┤
│ • Push to main/develop                                       │
│ • Pull Request                                               │
│ • Manual dispatch                                            │
│ • Scheduled (nightly)                                        │
│ • Tag creation (v*)                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    STAGE 1: LINTING                          │
│                    Duration: ~2 min                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Black   │  │  isort   │  │ Flake8   │  │  MyPy    │   │
│  │ Formato  │  │ Imports  │  │ PEP8     │  │  Types   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│      ✅            ✅            ✅            ⚠️           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    STAGE 2: TESTING                          │
│                    Duration: ~5 min                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│     Matrix Strategy (Parallel Execution)                    │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  Python 3.10    │  │  Python 3.11    │                  │
│  ├─────────────────┤  ├─────────────────┤                  │
│  │ Ubuntu  ✅      │  │ Ubuntu  ✅      │                  │
│  │ Windows ✅      │  │ Windows ✅      │                  │
│  │ macOS   ✅      │  │ macOS   ✅      │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                              │
│  ┌─────────────────┐                                        │
│  │  Python 3.12    │                                        │
│  ├─────────────────┤                                        │
│  │ Ubuntu  ✅      │                                        │
│  │ Windows ✅      │                                        │
│  │ macOS   ✅      │                                        │
│  └─────────────────┘                                        │
│                                                              │
│  Coverage: 87% ✅ (Target: 80%)                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  STAGE 3: SECURITY SCAN                      │
│                    Duration: ~3 min                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │   Safety Check     │    │   Bandit Scan      │          │
│  │  Dependencies      │    │   Code Security    │          │
│  │                    │    │                    │          │
│  │  ✅ 0 vulns        │    │  ⚠️ 2 warnings     │          │
│  └────────────────────┘    └────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    STAGE 4: BUILD                            │
│                    Duration: ~2 min                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  • Compile Python files (.pyc)                              │
│  • Verify imports                                           │
│  • Test Streamlit app syntax                                │
│  • Generate dependency report                               │
│                                                              │
│  Status: ✅ Build successful                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  STAGE 5: DEPLOYMENT                         │
│                    Duration: ~1 min                          │
│              (Only on 'main' branch)                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              ┌────────────────────┐                         │
│              │ Streamlit Cloud    │                         │
│              │                    │                         │
│              │ Auto-sync from     │                         │
│              │ GitHub main        │                         │
│              │                    │                         │
│              │ URL: app.streamlit │                         │
│              └────────────────────┘                         │
│                      ✅                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 6: NOTIFICATIONS                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ Pipeline Success!                                        │
│                                                              │
│  📧 Email: laura.munoz_pragma@...                           │
│  💬 Slack: #deployments                                     │
│  📊 Status: All checks passed                               │
│                                                              │
│  Total Duration: 13 minutes                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌊 Branching Strategy

```
main (production)
│
├─ v1.0.0 ─────┐ (tags trigger releases)
│              │
│              └─ 📦 GitHub Release
│
├─ commit ─────┐
│              ├─ ✅ Tests
│              ├─ ✅ Lint
│              ├─ ✅ Security
│              └─ 🚀 Deploy to Production
│
develop (staging)
│
├─ commit ─────┐
│              ├─ ✅ Tests
│              ├─ ✅ Lint
│              └─ 🧪 Deploy to Staging
│
feature/new-feature
│
└─ Pull Request ─┐
                 ├─ ✅ Tests
                 ├─ ✅ Lint
                 ├─ ✅ Security
                 ├─ 📊 Coverage Report
                 └─ ✍️ Code Review Required
```

---

## 📈 Pipeline Metrics Dashboard

```
╔════════════════════════════════════════════════════════════╗
║              PIPELINE PERFORMANCE METRICS                   ║
╠════════════════════════════════════════════════════════════╣
║                                                             ║
║  Success Rate:        ████████████████████░ 95%            ║
║  Average Duration:    █████████░░░░░░░░░░░ 13 min          ║
║  Failed Builds:       ██░░░░░░░░░░░░░░░░░░ 5%              ║
║  Coverage:            █████████████████░░░░ 87%            ║
║                                                             ║
║  Most Common Failures:                                      ║
║    1. Linting errors (45%)                                  ║
║    2. Test failures (30%)                                   ║
║    3. Coverage below threshold (15%)                        ║
║    4. Security warnings (10%)                               ║
║                                                             ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🔄 Development Workflow

```
┌─────────────┐
│  Developer  │
│   Writes    │
│    Code     │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│  Pre-commit     │◄────── BLACK, isort, flake8
│    Hooks        │        Run locally before commit
└──────┬──────────┘
       │
       ↓
┌─────────────────┐
│   Git Commit    │
└──────┬──────────┘
       │
       ↓
┌─────────────────┐
│   Git Push      │
└──────┬──────────┘
       │
       ↓
┌─────────────────────────────────────────┐
│         GitHub/GitLab Triggers          │
│              CI/CD Pipeline             │
└──────┬──────────────────────────────────┘
       │
       ├─────┐
       │     │
       ↓     ↓
   ┌─────┐ ┌─────┐
   │Lint │ │Test │ (Parallel)
   └──┬──┘ └──┬──┘
      │       │
      └───┬───┘
          │
          ↓
    ┌──────────┐
    │ Security │
    └────┬─────┘
         │
         ↓
    ┌──────────┐
    │  Build   │
    └────┬─────┘
         │
         ↓
    ┌──────────┐      ✅ main branch
    │  Deploy  │────► 🚀 Production
    └────┬─────┘      
         │            ⚠️ develop branch
         └──────────► 🧪 Staging
         
         
    ┌──────────┐
    │  Notify  │────► 📧 Email, 💬 Slack
    └──────────┘
```

---

## 🎯 Quality Gates

```
╔═══════════════════════════════════════════════════════════╗
║                    QUALITY GATES                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                            ║
║  Gate 1: Code Style                                        ║
║  ├─ Black formatting     ✅ PASS                          ║
║  ├─ Import ordering      ✅ PASS                          ║
║  └─ PEP8 compliance      ✅ PASS                          ║
║                                                            ║
║  Gate 2: Testing                                           ║
║  ├─ Unit tests           ✅ PASS (25/25)                  ║
║  ├─ Coverage >= 80%      ✅ PASS (87%)                    ║
║  └─ No test failures     ✅ PASS                          ║
║                                                            ║
║  Gate 3: Security                                          ║
║  ├─ No critical vulns    ✅ PASS                          ║
║  ├─ Dependency audit     ⚠️  WARN (2 minor)              ║
║  └─ Code security scan   ✅ PASS                          ║
║                                                            ║
║  Gate 4: Build                                             ║
║  ├─ Syntax valid         ✅ PASS                          ║
║  ├─ Imports resolve      ✅ PASS                          ║
║  └─ App starts           ✅ PASS                          ║
║                                                            ║
║  🎉 ALL GATES PASSED - READY TO DEPLOY                    ║
║                                                            ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🚨 Failure Scenarios & Recovery

```
Scenario 1: Tests Fail
────────────────────────────────────
❌ Test failure detected
  ↓
🔔 Developer notified via email
  ↓
🔍 Review test logs in GitHub Actions
  ↓
🛠️  Fix code locally
  ↓
🔄 Push fix
  ↓
✅ Pipeline re-runs automatically


Scenario 2: Coverage Below Threshold
────────────────────────────────────
⚠️  Coverage: 75% (threshold: 80%)
  ↓
📊 Coverage report generated
  ↓
🧪 Add missing tests
  ↓
✅ Coverage increases to 82%
  ↓
🎉 Pipeline passes


Scenario 3: Security Vulnerability
────────────────────────────────────
🔒 Critical vulnerability in requests==2.25.0
  ↓
🚨 Pipeline fails at security gate
  ↓
📦 Update: pip install requests==2.32.3
  ↓
✅ Security scan passes
  ↓
🚀 Continue to deployment


Scenario 4: Production Issue
────────────────────────────────────
🔥 Bug detected in production
  ↓
⚡ Immediate rollback:
   git revert <commit> && git push
  ↓
🔄 Pipeline deploys previous version
  ↓
🐛 Fix bug in hotfix branch
  ↓
✅ Test & merge hotfix
  ↓
🚀 Deploy fixed version
```

---

## 📦 Deployment Targets

```
┌───────────────────────────────────────────────────────┐
│                                                        │
│                  DEPLOYMENT MATRIX                     │
│                                                        │
├───────────────┬───────────────┬───────────────────────┤
│   Branch      │  Environment  │  Target               │
├───────────────┼───────────────┼───────────────────────┤
│   main        │  Production   │  Streamlit Cloud      │
│               │               │  (auto-deploy)        │
├───────────────┼───────────────┼───────────────────────┤
│   develop     │  Staging      │  Streamlit Cloud      │
│               │               │  (manual trigger)     │
├───────────────┼───────────────┼───────────────────────┤
│   feature/*   │  Preview      │  No deployment        │
│               │               │  (tests only)         │
├───────────────┼───────────────┼───────────────────────┤
│   v*.*.* tag  │  Release      │  GitHub Release +     │
│               │               │  Production           │
└───────────────┴───────────────┴───────────────────────┘
```

---

## 🔔 Notification Channels

```
┌──────────────────────────────────────────────────────┐
│                  NOTIFICATION FLOW                    │
└──────────────────────────────────────────────────────┘

Pipeline Start
     │
     ├──► 📧 Email: Pipeline started
     │
Pipeline Running
     │
     ├──► 💬 Slack: "Running tests..."
     │
Pipeline Complete
     │
     ├──[SUCCESS]──► ✅ Email: "Deploy successful"
     │               ✅ Slack: "🎉 Deployed to prod"
     │               ✅ GitHub: Green check mark
     │
     └──[FAILURE]──► ❌ Email: "Build failed"
                     ❌ Slack: "🚨 Pipeline failed"
                     ❌ GitHub: Red X mark
                     📝 Attach logs & error details
```

---

## 📊 CI/CD vs Manual Process

```
╔═══════════════════════════════════════════════════════════╗
║          MANUAL PROCESS vs AUTOMATED CI/CD                ║
╠═══════════════════════════════════════════════════════════╣
║                                                            ║
║  Manual Process (Before):                                  ║
║  ────────────────────────                                  ║
║  1. Developer writes code          (30 min)                ║
║  2. Manually run tests             (5 min)                 ║
║  3. Forgot to run linter           ❌                      ║
║  4. Push to production             (2 min)                 ║
║  5. Bug discovered in prod         🔥                      ║
║  6. Emergency hotfix               (60 min)                ║
║                                                            ║
║  Total: ~2 hours + stress                                  ║
║                                                            ║
║  ──────────────────────────────────────────               ║
║                                                            ║
║  CI/CD Process (After):                                    ║
║  ──────────────────────                                    ║
║  1. Developer writes code          (30 min)                ║
║  2. Pre-commit hooks auto-check    (10 sec)                ║
║  3. Push trigger CI/CD             (1 min)                 ║
║  4. Automated: lint + test + scan  (10 min)                ║
║  5. Issue found? Notified          ✅                      ║
║  6. Fix before production          ✅                      ║
║  7. Auto-deploy when ready         (2 min)                 ║
║                                                            ║
║  Total: ~45 min + peace of mind                            ║
║                                                            ║
║  Savings: 60% time + 90% fewer prod bugs                  ║
║                                                            ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎓 Learning Path

```
Week 1: Basics
├─ Day 1-2: Setup Git & GitHub/GitLab
├─ Day 3-4: Understand YAML syntax
├─ Day 5-6: First basic workflow
└─ Day 7: Run & debug

Week 2: Testing
├─ Day 1-2: Write unit tests
├─ Day 3-4: Coverage reporting
├─ Day 5-6: Integration tests
└─ Day 7: Test optimization

Week 3: Advanced
├─ Day 1-2: Security scanning
├─ Day 3-4: Multi-environment deploy
├─ Day 5-6: Notifications & monitoring
└─ Day 7: Performance tuning

Week 4: Mastery
├─ Day 1-2: Matrix strategies
├─ Day 3-4: Caching & optimization
├─ Day 5-6: Custom actions/jobs
└─ Day 7: Best practices review
```

---

## ✅ Quick Reference

```
╔════════════════════════════════════════════════════════╗
║              CI/CD COMMAND CHEATSHEET                   ║
╠════════════════════════════════════════════════════════╣
║                                                         ║
║  Local Development:                                     ║
║  ─────────────────                                      ║
║  pre-commit run --all-files    # Run hooks locally     ║
║  python -m pytest -v           # Run tests             ║
║  coverage run -m pytest        # With coverage         ║
║  black .                       # Format code           ║
║  flake8 seo_auditor/           # Lint code             ║
║                                                         ║
║  Git Operations:                                        ║
║  ───────────────                                        ║
║  git add . && git commit       # Stage & commit        ║
║  git push origin main          # Trigger CI/CD         ║
║  git tag v1.0.0                # Create release        ║
║  git push origin v1.0.0        # Trigger release       ║
║                                                         ║
║  GitHub CLI:                                            ║
║  ───────────                                            ║
║  gh run list                   # List workflow runs    ║
║  gh run view <id> --log        # View logs             ║
║  gh run rerun <id>             # Re-run workflow       ║
║                                                         ║
║  Debugging:                                             ║
║  ──────────                                             ║
║  act -l                        # List actions locally  ║
║  act push                      # Test workflow         ║
║                                                         ║
╚════════════════════════════════════════════════════════╝
```

---

**🎉 Your CI/CD Pipeline is Ready to Rock!**

For detailed instructions, see:
- [ANALISIS_CICD.md](ANALISIS_CICD.md)
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [CICD_BEST_PRACTICES.md](CICD_BEST_PRACTICES.md)
