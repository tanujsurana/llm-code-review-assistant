from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import CodeReview
from app.github_service import get_pull_request_diff, post_comment_to_pr
from app.llm_service import review_code_with_llm

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Code Review Assistant")


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/webhook/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    event_type = request.headers.get("X-GitHub-Event")

    # GitHub sends a ping event when webhook is created
    if event_type == "ping":
        return {"message": "GitHub webhook ping received successfully"}

    # Only process pull_request events
    if event_type != "pull_request":
        return {"message": f"Ignored event: {event_type}"}

    action = payload.get("action")

    if action not in ["opened", "synchronize", "reopened"]:
        return {"message": f"Ignored pull request action: {action}"}

    pull_request = payload.get("pull_request")
    repository = payload.get("repository")

    if not pull_request or not repository:
        raise HTTPException(status_code=400, detail="Invalid GitHub webhook payload")

    pr_number = pull_request["number"]
    repo_full_name = repository["full_name"]
    commit_sha = pull_request["head"]["sha"]

    diff_text = get_pull_request_diff(repo_full_name, pr_number)

    review_result = review_code_with_llm(diff_text)

    review_record = CodeReview(
        repo_name=repo_full_name,
        pr_number=pr_number,
        commit_sha=commit_sha,
        diff_text=diff_text,
        review_result=review_result,
    )

    db.add(review_record)
    db.commit()
    db.refresh(review_record)

    try:
        post_comment_to_pr(repo_full_name, pr_number, review_result)
    except Exception as e:
        return {
            "message": "Review completed and saved, but failed to post GitHub comment",
            "review_id": review_record.id,
            "error": str(e),
        }

    return {
        "message": "Review completed",
        "review_id": review_record.id,
    }


@app.get("/reviews")
def get_reviews(db: Session = Depends(get_db)):
    return db.query(CodeReview).all()
