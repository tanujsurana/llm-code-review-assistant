from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def review_code_with_llm(diff_text: str) -> str:
    if len(diff_text) > 12000:
        diff_text = diff_text[:12000]

    prompt = f"""
You are a senior backend engineer reviewing a GitHub pull request.

Review this PR diff and give concise, useful feedback.

Return your answer in this format:

### Summary
Briefly explain what changed.

### Bugs or Logic Issues
List any possible bugs.

### Security Concerns
Mention security risks if any.

### Performance Concerns
Mention performance issues if any.

### Code Quality Suggestions
Give practical improvement suggestions.

### Final Recommendation
Approve, request changes, or needs human review.

PR Diff:
{diff_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a careful senior software engineer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
