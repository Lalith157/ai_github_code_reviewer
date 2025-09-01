import subprocess
import tempfile
import os

def run_linters(filename, patch_content):
    issues = []
    ext = os.path.splitext(filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(patch_content.encode())
        tmp_path = tmp.name

    if ext == ".py":
        result = subprocess.run(["pylint", tmp_path], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append(result.stdout)
    elif ext in [".js", ".ts"]:
        result = subprocess.run(["eslint", tmp_path], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append(result.stdout)
    elif ext in [".c", ".cpp"]:
        result = subprocess.run(["gcc", "-fsyntax-only", tmp_path], capture_output=True, text=True)
        if result.returncode != 0:
            issues.append(result.stderr)

    return issues
