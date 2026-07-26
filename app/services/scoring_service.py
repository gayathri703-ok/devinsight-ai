CATEGORY_WEIGHTS = {
    "documentation": 15,
    "activity": 20,
    "testing": 20,
    "code_structure": 15,
    "popularity": 15,
    "security": 15,
}


def calculate_health_score(category_scores: dict) -> dict:
    total_score = 0
    breakdown = {}

    for category, weight in CATEGORY_WEIGHTS.items():
        raw_score = category_scores.get(category, 0)
        weighted_contribution = (raw_score / 100) * weight
        total_score += weighted_contribution

        breakdown[category] = {
            "raw_score": raw_score,
            "weight": weight,
            "contribution": round(weighted_contribution, 2),
        }

    return {
        "health_score": round(total_score, 2),
        "breakdown": breakdown,
    }