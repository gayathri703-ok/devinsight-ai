import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def test_connection() -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": "Say hello in one short sentence, mentioning you're helping analyze a GitHub repository."}
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content


def generate_project_summary(owner: str, repo: str, analysis_data: dict) -> dict:
    prompt = f"""You are analyzing the GitHub repository {owner}/{repo}.

Here is the data collected about it:
- Health Score: {analysis_data.get('health_score')}/100
- Documentation: {analysis_data['details']['documentation']}
- Activity: {analysis_data['details']['activity']}
- Code Quality: {analysis_data['details']['code_quality']}
- Popularity: {analysis_data['details']['popularity']}
- Primary Language: {analysis_data.get('primary_language', 'Unknown')}
- Languages: {analysis_data.get('languages', {})}

Respond with ONLY valid JSON (no markdown, no extra text) in this exact format:
{{
  "overview": "2-3 sentences describing overall project health",
  "tech_stack_explanation": "1-2 sentences explaining what technologies this project uses and why, based on the languages data",
  "strongest_area": "1 sentence naming the strongest category and why",
  "weakest_area": "1 sentence naming the weakest category and why",
  "improvement_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)