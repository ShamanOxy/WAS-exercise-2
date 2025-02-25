#!/usr/bin/env python3
"""
Creates a ZIP archive of the submission files for uploading to Canvas.
Automatically commits and pushes all changes before creating the archive.

Usage:
    python3 scripts/submit_zip.py
"""

import datetime
import os
import subprocess
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUBMISSION_DIRS = ["task-1", "task-2", "task-3"]
SUBMISSION_FILES = ["EXERCISE.md", "README.md"]
EXCLUDE_PATTERNS = ["__pycache__", ".pyc", ".pyo", "benchmarks/"]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)


def git_commit_and_push():
    print("--- Git: checking status ---")
    status = run(["git", "status", "--porcelain"])
    if not status.stdout.strip():
        print("No changes to commit.")
    else:
        print("Staging all changes...")
        run(["git", "add", "-A"])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Submission {timestamp}"
        print(f"Committing: {msg}")
        result = run(["git", "commit", "-m", msg])
        if result.returncode != 0:
            print(f"Commit failed:\n{result.stderr}")
            return False
        print("Committed successfully.")

    print("\n--- Git: pushing to remote ---")
    result = run(["git", "push"])
    if result.returncode != 0:
        print(f"Push failed:\n{result.stderr}")
        print("You can push manually with: git push")
        return False
    print("Pushed successfully.")
    return True


def get_commit_info():
    result = run(["git", "log", "-1", "--format=%H%n%s%n%ai"])
    if result.returncode == 0:
        lines = result.stdout.strip().split("\n")
        return {
            "hash": lines[0] if len(lines) > 0 else "unknown",
            "message": lines[1] if len(lines) > 1 else "unknown",
            "date": lines[2] if len(lines) > 2 else "unknown",
        }
    return {"hash": "unknown", "message": "unknown", "date": "unknown"}


def get_remote_url():
    result = run(["git", "remote", "get-url", "origin"])
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def should_exclude(path):
    return any(pattern in path for pattern in EXCLUDE_PATTERNS)


def main():
    print("=" * 50)
    print("Exercise 2: ZIP Submission")
    print("=" * 50)
    print()

    git_commit_and_push()

    commit = get_commit_info()
    remote = get_remote_url()

    zip_name = "submission-exercise-2.zip"
    zip_path = os.path.join(REPO_ROOT, zip_name)

    print(f"\n--- Creating ZIP: {zip_name} ---")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        cover = (
            f"Exercise 2: Automated Planning — Submission\n"
            f"{'=' * 50}\n\n"
            f"Repository:  {remote}\n"
            f"Commit:      {commit['hash']}\n"
            f"Message:     {commit['message']}\n"
            f"Date:        {commit['date']}\n"
        )
        zf.writestr("SUBMISSION_INFO.txt", cover)

        for f in SUBMISSION_FILES:
            fpath = os.path.join(REPO_ROOT, f)
            if os.path.isfile(fpath):
                zf.write(fpath, f)
                print(f"  + {f}")

        for d in SUBMISSION_DIRS:
            dirpath = os.path.join(REPO_ROOT, d)
            if not os.path.isdir(dirpath):
                print(f"  ! {d}/ not found, skipping")
                continue
            for root, dirs, files in os.walk(dirpath):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, REPO_ROOT)
                    if should_exclude(arcname):
                        continue
                    zf.write(filepath, arcname)
                    print(f"  + {arcname}")

    print(f"\nZIP created: {zip_path}")
    print()
    print("=" * 50)
    print(f"Upload '{zip_name}' to Canvas.")
    print("=" * 50)


if __name__ == "__main__":
    main()
