# 🛡️ AI-PR Guardian Demo

> **Zero-cost, fully automated security scanner for pull requests**

A GitHub Actions-based bot that automatically scans PRs for security violations, hardcoded secrets, and compliance issues. **100% free** using GitHub's free tier.

## ✨ Features

- ✅ **Automated PR Scanning** - Triggers on every PR open/update
- ✅ **Policy Engine** - YAML-based customizable rules
- ✅ **Secret Detection** - Finds API keys, tokens, passwords
- ✅ **Dangerous Function Blocking** - Detects eval(), exec(), etc.
- ✅ **Real-time Comments** - Auto-comments on PRs with violations
- ✅ **Zero Cost** - Uses only GitHub Actions (free tier)

## 🧪 Test It Right Now!

### **Test 1: Create a PR with Violations** ⚠️

```bash
git checkout -b test-violations
cp examples/bad_code_examples/vulnerable_app.py app.py
git add app.py
git commit -m "Add app with intentional security violations"
git push origin test-violations
