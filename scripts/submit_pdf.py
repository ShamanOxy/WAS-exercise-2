#!/usr/bin/env python3
"""
Creates a PDF of the submission for uploading to Canvas.
Automatically commits and pushes all changes before creating the PDF.

Generates a single PDF containing all submission files with syntax highlighting
using only Python standard library (no external dependencies).

Usage:
    python3 scripts/submit_pdf.py
"""

import datetime
import html
import os
import subprocess
import tempfile
import webbrowser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUBMISSION_DIRS = ["task-1", "task-2", "task-3"]
SUBMISSION_FILES = ["README.md"]
EXCLUDE_PATTERNS = ["__pycache__", ".pyc", ".pyo", "benchmarks/", ".soln"]

# File extensions to include as source code
CODE_EXTENSIONS = {".py", ".pddl", ".md"}

# Only include these Python files (the ones that originally had TODOs)
INCLUDE_PY_FILES = {"task.py", "a_star.py"}


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


def collect_files():
    """Collect all submission files."""
    files = []
    for f in SUBMISSION_FILES:
        fpath = os.path.join(REPO_ROOT, f)
        if os.path.isfile(fpath):
            files.append(f)

    for d in SUBMISSION_DIRS:
        dirpath = os.path.join(REPO_ROOT, d)
        if not os.path.isdir(dirpath):
            continue
        for root, dirs, filenames in os.walk(dirpath):
            for filename in sorted(filenames):
                filepath = os.path.join(root, filename)
                arcname = os.path.relpath(filepath, REPO_ROOT)
                if should_exclude(arcname):
                    continue
                _, ext = os.path.splitext(filename)
                if ext == ".py" and filename not in INCLUDE_PY_FILES:
                    continue
                if ext in CODE_EXTENSIONS:
                    files.append(arcname)
    return files


def generate_html(files, commit, remote):
    """Generate an HTML document with all submission files."""
    parts = []
    parts.append("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Exercise 2: Submission</title>
<style>
  @media print {
    .file-section { page-break-before: always; }
    .file-section:first-of-type { page-break-before: avoid; }
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 2cm;
    font-size: 11pt;
    color: #1a1a1a;
  }
  .cover {
    text-align: center;
    padding: 4cm 0 2cm 0;
  }
  .cover h1 { font-size: 24pt; margin-bottom: 0.5em; }
  .cover .meta {
    font-size: 10pt;
    color: #555;
    margin-top: 2em;
    text-align: left;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
  }
  .cover .meta td { padding: 2px 8px; }
  .cover .meta td:first-child { font-weight: bold; }
  .file-section h2 {
    font-size: 13pt;
    background: #f0f0f0;
    padding: 6px 12px;
    border-radius: 4px;
    font-family: monospace;
  }
  pre {
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 12px;
    font-size: 9pt;
    line-height: 1.4;
    overflow-wrap: break-word;
    white-space: pre-wrap;
  }
  .line-num {
    color: #999;
    user-select: none;
    display: inline-block;
    width: 3.5em;
    text-align: right;
    margin-right: 1em;
  }
</style>
</head>
<body>
""")

    # Cover page
    parts.append(f"""
<div class="cover">
  <h1>Exercise 2: Automated Planning</h1>
  <p>Submission</p>
  <table class="meta">
    <tr><td>Repository</td><td>{html.escape(remote)}</td></tr>
    <tr><td>Commit</td><td><code>{html.escape(commit['hash'][:12])}</code></td></tr>
    <tr><td>Message</td><td>{html.escape(commit['message'])}</td></tr>
    <tr><td>Date</td><td>{html.escape(commit['date'])}</td></tr>
  </table>
</div>
""")

    # File contents
    for filepath in files:
        fullpath = os.path.join(REPO_ROOT, filepath)
        try:
            with open(fullpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            content = "(binary or unreadable file)"

        parts.append(f'<div class="file-section">')
        parts.append(f"<h2>{html.escape(filepath)}</h2>")
        parts.append("<pre>")
        for i, line in enumerate(content.split("\n"), 1):
            parts.append(
                f'<span class="line-num">{i}</span>{html.escape(line)}'
            )
        parts.append("</pre>")
        parts.append("</div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    print("=" * 50)
    print("Exercise 2: PDF Submission")
    print("=" * 50)
    print()

    git_commit_and_push()

    commit = get_commit_info()
    remote = get_remote_url()
    files = collect_files()

    print(f"\n--- Generating PDF ({len(files)} files) ---")
    for f in files:
        print(f"  + {f}")

    html_content = generate_html(files, commit, remote)

    html_path = os.path.join(REPO_ROOT, "submission-exercise-2.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\nHTML created: {html_path}")
    print()
    print("=" * 50)
    print("To create the PDF:")
    print(f"  1. The file has been opened in your browser.")
    print(f"  2. Press Ctrl+P / Cmd+P to print.")
    print(f"  3. Select 'Save as PDF' as the destination.")
    print(f"  4. Upload the PDF to Canvas.")
    print("=" * 50)

    webbrowser.open(f"file://{html_path}")


if __name__ == "__main__":
    main()
