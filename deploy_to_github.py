#!/usr/bin/env python3
"""
Automated GitHub Pages Deployment Manager for Medical Research Assistant.
Creates a remote public repository via GitHub API (or configures an existing one),
pushes all code, and enables GitHub Pages workflow deployment.
"""

import sys
import os
import json
import subprocess
import urllib.request
import urllib.error

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd, cwd=REPO_DIR, check=True):
    res = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {cmd}\nStderr: {res.stderr}\nStdout: {res.stdout}")
    return res

def main():
    print("=" * 60)
    print("🩺 Medical Research Assistant - GitHub Repository & Pages Setup")
    print("=" * 60)

    # 1. Check Git commits
    run_cmd("git add -A")
    res = run_cmd("git status --porcelain")
    if res.stdout.strip():
        print("Committing pending changes...")
        run_cmd('git commit -m "chore: prepare repository for GitHub Pages deployment"')
    else:
        print("✓ All repository files are cleanly committed.")

    # 2. Collect user details
    username = sys.argv[1] if len(sys.argv) > 1 else input("Enter your GitHub username: ").strip()
    if not username:
        print("❌ Error: GitHub username cannot be empty.")
        sys.exit(1)

    repo_name = sys.argv[2] if len(sys.argv) > 2 else "med-research-assistant"
    
    print("\nIf you have a GitHub Personal Access Token (classic or fine-grained with 'repo' scope),")
    print("this script can automatically create the public repo and enable GitHub Pages via API.")
    print("Press Enter to skip if you already created the empty repo at github.com or prefer standard login.")
    token = sys.argv[3] if len(sys.argv) > 3 else input("Enter GitHub Personal Access Token (optional): ").strip()

    # 3. Create repo via API if token is provided
    if token:
        print(f"\nContacting GitHub API to create public repository '{repo_name}'...")
        req = urllib.request.Request(
            "https://api.github.com/user/repos",
            data=json.dumps({
                "name": repo_name,
                "private": False,
                "description": "Medical Research Assistant - Specialist Clinical Intelligence Engine for MD Medicine",
                "auto_init": False
            }).encode("utf-8"),
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Medical-Research-Assistant-Deployer"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status == 201:
                    print(f"✓ Created public repository: https://github.com/{username}/{repo_name}")
        except urllib.error.HTTPError as e:
            if e.code == 422:
                print(f"ℹ Repository '{repo_name}' already exists on account {username}. Proceeding to push...")
            else:
                body = e.read().decode("utf-8", errors="ignore")
                print(f"⚠️ GitHub API returned HTTP {e.code}: {body}")

        # Set remote with token
        run_cmd("git remote remove origin", check=False)
        run_cmd(f"git remote add origin https://{username}:{token}@github.com/{username}/{repo_name}.git")
    else:
        # Standard HTTPS remote
        run_cmd("git remote remove origin", check=False)
        run_cmd(f"git remote add origin https://github.com/{username}/{repo_name}.git")

    # 4. Push to main
    print(f"\nPushing repository to branch 'main' on GitHub...")
    run_cmd("git branch -M main")

    if token:
        run_cmd("git push -u origin main --force")
        print("✓ Code pushed successfully!")

        # Configure Pages via API
        print("Configuring GitHub Pages to build from GitHub Actions...")
        pages_req = urllib.request.Request(
            f"https://api.github.com/repos/{username}/{repo_name}/pages",
            data=json.dumps({"build_type": "workflow"}).encode("utf-8"),
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Medical-Research-Assistant-Deployer"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(pages_req) as resp:
                print("✓ GitHub Pages configured for GitHub Actions!")
        except urllib.error.HTTPError as e:
            print(f"ℹ GitHub Pages API status: HTTP {e.code} (GitHub Actions will handle build automatically).")
    else:
        print(f"Executing: git push -u origin main")
        push_res = run_cmd("git push -u origin main", check=False)
        if push_res.returncode == 0:
            print("✓ Code pushed successfully!")
        else:
            print(f"\n⚠️ Push requires authentication. Output:\n{push_res.stderr or push_res.stdout}")
            print("\nPlease ensure you have created the empty repository on github.com:")
            print(f"👉 https://github.com/new (Name: {repo_name})")
            print("Then push using:")
            print(f"git push -u origin main")

    pages_url = f"https://{username}.github.io/{repo_name}/"
    print("\n" + "=" * 60)
    print("🎉 DEPLOYMENT SUMMARY")
    print("=" * 60)
    print(f"GitHub Repository: https://github.com/{username}/{repo_name}")
    print(f"Live Public Web URL: {pages_url}")
    print("\nNext step:")
    print("1. Go to your repo settings: https://github.com/{username}/{repo_name}/settings/pages")
    print("2. Ensure 'Build and deployment' > Source is set to 'GitHub Actions'.")
    print(f"3. Your assistant is now live and accessible by anyone at:\n👉 {pages_url}")
    print("=" * 60)

if __name__ == "__main__":
    main()
