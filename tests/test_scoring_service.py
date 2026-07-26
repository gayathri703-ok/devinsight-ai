from app.services.scoring_service import calculate_health_score


def test_perfect_score():
    scores = {
        "documentation": 100,
        "activity": 100,
        "testing": 100,
        "code_structure": 100,
        "popularity": 100,
        "security": 100,
    }
    result = calculate_health_score(scores)
    assert result["health_score"] == 100.0


def test_zero_score():
    scores = {
        "documentation": 0,
        "activity": 0,
        "testing": 0,
        "code_structure": 0,
        "popularity": 0,
        "security": 0,
    }
    result = calculate_health_score(scores)
    assert result["health_score"] == 0.0


def test_known_result():
    # Same values you manually verified back on Day 8
    scores = {
        "documentation": 80,
        "activity": 90,
        "testing": 40,
        "code_structure": 70,
        "popularity": 100,
        "security": 60,
    }
    result = calculate_health_score(scores)
    assert result["health_score"] == 72.5


def test_missing_category_defaults_to_zero():
    scores = {
        "documentation": 100,
        # all other categories missing
    }
    result = calculate_health_score(scores)
    assert result["breakdown"]["activity"]["raw_score"] == 0