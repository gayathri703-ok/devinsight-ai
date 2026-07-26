from app.services import github_service

TEST_FOLDER_NAMES = {"tests", "test", "__tests__"}
LINT_CONFIG_FILES = {".eslintrc", ".eslintrc.json", ".flake8", "pyproject.toml", ".pylintrc"}
PACKAGE_FILES = {"requirements.txt", "package.json", "pyproject.toml", "Pipfile", "pom.xml"}


def analyze_code_quality(owner: str, repo: str) -> dict:
    root_contents = github_service.fetch_repo_contents(owner, repo)
    root_names = {item["name"] for item in root_contents}

    has_tests = any(name.lower() in TEST_FOLDER_NAMES for name in root_names)
    has_lint_config = any(name in LINT_CONFIG_FILES for name in root_names)
    has_package_file = any(name in PACKAGE_FILES for name in root_names)

    workflows = github_service.fetch_repo_contents(owner, repo, path=".github/workflows")
    has_ci = len(workflows) > 0

    score = 0
    if has_tests:
        score += 40
    if has_ci:
        score += 30
    if has_lint_config:
        score += 15
    if has_package_file:
        score += 15

    return {
        "has_tests": has_tests,
        "has_ci": has_ci,
        "has_lint_config": has_lint_config,
        "has_package_file": has_package_file,
        "code_quality_score": score,
    }