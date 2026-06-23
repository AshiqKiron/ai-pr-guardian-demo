
---

### 10. `docs/QUICK_START.md`

```markdown
# 🚀 Quick Start Guide

## Step 1: Enable GitHub Actions
1. Go to Settings → Actions → General
2. Select "Allow all actions and reusable workflows"

## Step 2: Test with Bad Code
```bash
git checkout -b test-violations
cp examples/bad_code_examples/vulnerable_app.py app.py
git add app.py
git commit -m "Test: Add code with violations"
git push origin test-violations
