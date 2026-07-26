import re
from app.services import github_service

SENSITIVE_FILENAME_PATTERNS = {
    "id_rsa", "id_dsa", ".pem", ".key", "credentials.json",
    "secrets.json", ".pfx", ".p12", "aws_credentials",
}

LARGE_FILE_THRESHOLD_BYTES = 5_000_000  # 5 MB

SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Generic API Key": re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]"),
    "Generic Secret": re.compile(r"(?i)(secret|password|token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{12,}['\"]"),
    "Private Key Header": re.compile(r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----"),
}

FILES_TO_SCAN = [".env", "config.py", "settings.py", "config.json", ".env.local"]

SEVERITY_PENALTIES = {
    "critical": 40,
    "high": 25,
    "medium": 15,
    "low": 5,
}


def check_missing_readme(owner: str, repo: str) -> dict:
    has_readme = github_service.check_readme_exists(owner, repo)
    return {
        "check": "missing_readme",
        "passed": has_readme,
        "severity": "medium" if not has_readme else None,
        "message": "README is present." if has_readme else "No README found - reduces project transparency and trust.",
    }


def check_missing_license(owner: str, repo: str) -> dict:
    repo_data = github_service.fetch_repo_details(owner, repo)
    has_license = repo_data.get("license") is not None
    return {
        "check": "missing_license",
        "passed": has_license,
        "severity": "low" if not has_license else None,
        "message": "License is present." if has_license else "No license found - legal usage terms are unclear.",
    }


def check_large_files(owner: str, repo: str) -> dict:
    contents = github_service.fetch_repo_contents(owner, repo)
    large_files = [
        item["name"] for item in contents
        if item.get("type") == "file" and item.get("size", 0) > LARGE_FILE_THRESHOLD_BYTES
    ]

    passed = len(large_files) == 0
    return {
        "check": "large_files",
        "passed": passed,
        "severity": "low" if not passed else None,
        "message": "No unusually large files in root directory." if passed
                    else f"Found {len(large_files)} large file(s) in root: {', '.join(large_files)}",
    }


def check_sensitive_filenames(owner: str, repo: str) -> dict:
    contents = github_service.fetch_repo_contents(owner, repo)
    flagged_files = [
        item["name"] for item in contents
        if any(pattern in item["name"].lower() for pattern in SENSITIVE_FILENAME_PATTERNS)
    ]

    passed = len(flagged_files) == 0
    return {
        "check": "sensitive_filenames",
        "passed": passed,
        "severity": "high" if not passed else None,
        "message": "No sensitive filenames detected." if passed
                    else f"Potentially sensitive file(s) found: {', '.join(flagged_files)}",
    }


def check_exposed_secrets(owner: str, repo: str) -> dict:
    findings = []

    for file_path in FILES_TO_SCAN:
        content = github_service.fetch_file_content(owner, repo, file_path)
        if content is None:
            continue

        for secret_type, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                findings.append({"file": file_path, "type": secret_type})

    passed = len(findings) == 0
    return {
        "check": "exposed_secrets",
        "passed": passed,
        "severity": "critical" if not passed else None,
        "message": "No exposed secrets detected in scanned files." if passed
                    else f"Potential secrets found: {findings}",
    }


def run_basic_security_checks(owner: str, repo: str) -> dict:
    checks = [
        check_missing_readme(owner, repo),
        check_missing_license(owner, repo),
        check_large_files(owner, repo),
        check_sensitive_filenames(owner, repo),
        check_exposed_secrets(owner, repo),
    ]

    failed_checks = [c for c in checks if not c["passed"]]

    return {
        "checks": checks,
        "total_checks": len(checks),
        "passed_checks": len(checks) - len(failed_checks),
        "failed_checks": len(failed_checks),
    }


def calculate_security_score(checks: list[dict]) -> int:
    score = 100
    for check in checks:
        if not check["passed"] and check["severity"]:
            score -= SEVERITY_PENALTIES.get(check["severity"], 10)
    return max(score, 0)


def generate_security_report(owner: str, repo: str) -> dict:
    checks = [
        check_missing_readme(owner, repo),
        check_missing_license(owner, repo),
        check_large_files(owner, repo),
        check_sensitive_filenames(owner, repo),
        check_exposed_secrets(owner, repo),
    ]

    failed_checks = [c for c in checks if not c["passed"]]
    security_score = calculate_security_score(checks)

    return {
        "security_score": security_score,
        "checks": checks,
        "total_checks": len(checks),
        "passed_checks": len(checks) - len(failed_checks),
        "failed_checks": len(failed_checks),
    }