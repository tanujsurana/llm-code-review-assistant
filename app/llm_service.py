from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def review_code_with_llm(diff_text: str) -> str:
    prompt = f"""
You are a senior software engineer reviewing a GitHub pull request.

Review the following code diff and provide feedback in this format:

1. Summary
2. Possible Bugs
3. Security Issues
4. Performance Concerns
5. Code Quality Suggestions
6. Final Recommendation

Code diff:
{diff_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert backend code reviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
