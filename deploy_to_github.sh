#!/bin/bash
# ==============================================================================
# Automated Deployment Script for Medical Research Assistant -> GitHub Pages
# ==============================================================================

set -e

REPO_DIR="/Users/user/med-research-assistant"
cd "$REPO_DIR"

echo "========================================================"
echo "🩺 Medical Research Assistant - GitHub Pages Deployment"
echo "========================================================"

# 1. Verify Git status
if [ ! -d ".git" ]; then
    echo "Initializing local Git repository..."
    git init
    git branch -M main
fi

# Ensure all files are committed
git add -A
if ! git diff --cached --quiet; then
    echo "Committing pending changes..."
    git commit -m "chore: prepare repository for GitHub Pages deployment"
else
    echo "✓ All files are cleanly staged and committed."
fi

# 2. Get GitHub details
USERNAME="$1"
REPO_NAME="${2:-med-research-assistant}"
GITHUB_TOKEN="$3"

if [ -z "$USERNAME" ]; then
    read -p "Enter your GitHub username: " USERNAME
fi

if [ -z "$USERNAME" ]; then
    echo "❌ Error: GitHub username is required."
    exit 1
fi

echo ""
echo "Target Repository: https://github.com/$USERNAME/$REPO_NAME"
echo ""

# 3. Create repository via GitHub API if token is provided
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Authenticating with GitHub API via provided token..."
    CREATE_RESP=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$REPO_NAME\",\"private\":false,\"description\":\"Medical Research Assistant - Specialist Clinical Intelligence Engine for MD Medicine\",\"auto_init\":false}")

    HTTP_STATUS=$(echo "$CREATE_RESP" | tail -n1)
    BODY=$(echo "$CREATE_RESP" | head -n -1)

    if [ "$HTTP_STATUS" -eq 201 ]; then
        echo "✓ Public GitHub repository '$REPO_NAME' created successfully!"
    elif [ "$HTTP_STATUS" -eq 422 ]; then
        echo "ℹ Repository '$REPO_NAME' already exists on your account. Proceeding to push..."
    else
        echo "⚠️ Note: API returned HTTP $HTTP_STATUS ($BODY). Will attempt standard push."
    fi

    # Set authenticated remote URL
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://$USERNAME:$GITHUB_TOKEN@github.com/$USERNAME/$REPO_NAME.git"
else
    # Set standard HTTPS remote
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"
fi

# 4. Push to main branch
echo "Pushing code to branch 'main' on GitHub..."
git branch -M main

if [ -n "$GITHUB_TOKEN" ]; then
    git push -u origin main --force
    # Configure GitHub Pages via API to use GitHub Actions workflow
    echo "Configuring GitHub Pages to build from GitHub Actions..."
    curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$USERNAME/$REPO_NAME/pages" \
        -d '{"build_type":"workflow"}' > /dev/null || true
else
    echo "Please authenticate with GitHub when prompted:"
    git push -u origin main
fi

PAGES_URL="https://$USERNAME.github.io/$REPO_NAME/"

echo ""
echo "========================================================"
echo "🎉 DEPLOYMENT INITIATED SUCCESSFULLY!"
echo "========================================================"
echo "Repository: https://github.com/$USERNAME/$REPO_NAME"
echo "Public Live URL: $PAGES_URL"
echo ""
echo "The GitHub Actions workflow (.github/workflows/deploy.yml) will"
echo "now build and publish your site automatically."
echo "Your live site will be accessible from anywhere at:"
echo "👉 $PAGES_URL"
echo "========================================================"
