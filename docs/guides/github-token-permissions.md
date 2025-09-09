<!--
@meta
id: document_20250905_1110_github-token-permissions
type: document
scope: operational
status: archived
created: 2025-09-05
updated: 2025-09-05
tags: guides, github, github-token-permissions.md, token, permissions
related: 
-->

# GitHub Token Permissions Guide

## 🔄 Slash Command Policy (v30.3+)

**Korean-only Commands:** Starting from v30.3, the toolkit uses Korean slash commands exclusively:
- `/기획`, `/구현`, `/안정화`, `/배포` 등
- **Rationale:** Claude Code now fully supports Korean filenames
- **Benefits:** Simplified codebase, no duplicate maintenance

## Overview
This guide explains the GitHub token permissions required for full Claude Dev Kit functionality, especially Branch Protection setup.

## Token Types

### 1. Personal Access Token (Classic)
**Recommended for simplicity**

#### Required Scopes:
- `repo` - Full repository access (for basic operations)
- `admin:repo` - Repository administration (for Branch Protection)
- `workflow` - GitHub Actions workflow access (optional but recommended)

#### How to Create:
1. Go to Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (all sub-items)
   - ✅ `admin:repo` (specifically `admin:repo_hook`)
   - ✅ `workflow` (optional)
4. Generate token and save it securely

### 2. Fine-grained Personal Access Token
**More secure but complex**

#### Required Permissions:
- **Repository permissions:**
  - Contents: Read & Write
  - Actions: Read
  - Administration: Write (for Branch Protection)
  - Pull requests: Read & Write
  - Issues: Read & Write

#### Repository Access:
- Can be configured for:
  - All repositories (simpler but broader access)
  - Selected repositories (more secure, needs updating for new repos)

#### How to Create:
1. Go to Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Click "Generate new token"
3. Select repository access:
   - "Selected repositories" and add each repo you'll use
   - Or "All repositories" for convenience
4. Set permissions as listed above
5. Generate token

## Common Issues

### 1. "Resource not accessible by personal access token"
**Cause:** Token lacks `admin:repo` scope (Classic) or `Administration: write` (Fine-grained)

**Solution:**
- Classic token: Regenerate with `admin:repo` scope
- Fine-grained: Edit token to add Administration: write permission

### 2. Multiple Token Conflicts
**Symptom:** Different behaviors with `gh` CLI vs environment variables

**Check current setup:**
```bash
# Check which token is active
gh auth status

# Check environment variable
echo $GH_TOKEN | cut -c1-10...  # Shows first 10 chars

# Check gh config token
gh auth token | cut -c1-10...
```

**Solution:**
```bash
# Use consistent token
export GH_TOKEN=$(gh auth token)

# Or re-login with correct token
gh auth logout
gh auth login
```

### 3. Fine-grained Token Repository Limits
**Issue:** Need to add each new repository manually

**Solutions:**
1. Use "All repositories" access (less secure)
2. Update token when creating new repos
3. Use Classic token for simpler management

## Recommendations

### For Individual Developers:
- **Use Classic Token with `admin:repo` scope**
- Simple, works everywhere, no per-repo configuration

### For Teams/Organizations:
- **Use Fine-grained tokens with selected repositories**
- Better security, audit trail, principle of least privilege

### For CI/CD:
- **Use GitHub App or deploy keys**
- Avoid personal tokens in automated systems

## Checking Your Current Token

```bash
# Check token permissions
gh api user -H "Accept: application/vnd.github.v3+json" | jq '.permissions'

# Test Branch Protection access
gh api repos/OWNER/REPO/branches/main/protection 2>&1 | head -1
# Success: Shows protection rules
# Failure: "Resource not accessible by personal access token"
```

## Quick Fix Script

```bash
#!/bin/bash
# Quick token permission check

echo "🔍 Checking GitHub token permissions..."

# Check if gh is authenticated
if ! gh auth status &>/dev/null; then
    echo "❌ Not authenticated. Run: gh auth login"
    exit 1
fi

# Try to access branch protection
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)
if [ -z "$REPO" ]; then
    echo "⚠️ Not in a GitHub repository"
    exit 1
fi

echo "Testing repository: $REPO"

# Test branch protection access
if gh api "repos/$REPO/branches/main/protection" &>/dev/null; then
    echo "✅ Token has admin:repo permission"
else
    echo "❌ Token lacks admin:repo permission"
    echo ""
    echo "To fix:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Edit your token or create new one"
    echo "3. Add 'admin:repo' scope (Classic) or 'Administration: write' (Fine-grained)"
fi
```

## Security Best Practices

1. **Never commit tokens** to repositories
2. **Use environment variables** for tokens
3. **Rotate tokens regularly** (every 90 days)
4. **Use minimal required permissions**
5. **Use separate tokens** for different purposes
6. **Enable SSO** if using organization repos

## Alternative: Manual Branch Protection

If token permissions cannot be changed:

```bash
# Use init.sh without Branch Protection
./init.sh --upgrade

# Manually configure in GitHub UI:
# 1. Go to Settings → Branches
# 2. Add rule for 'main'
# 3. Enable required status checks
# 4. Select TADD enforcement checks
```

---

For more help, see the [GitHub Token Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)