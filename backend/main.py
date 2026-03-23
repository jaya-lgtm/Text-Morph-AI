from fastapi import FastAPI
from bson import ObjectId
from passlib.context import CryptContext
from backend.database import get_users_collection, get_history_collection, create_indexes
from backend.models import User, TextData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

create_indexes()


@app.post("/signup")
def signup(user: User):
    users_col = get_users_collection()
    try:
        hashed_password = pwd_context.hash(user.password)
        users_col.insert_one({
            "username": user.username,
            "password": hashed_password,
            "display_name": user.display_name or user.username
        })
        return {"status": "success"}
    except Exception:
        return {"status": "error", "message": "User already exists"}


@app.post("/login")
def login(user: User):
    users_col = get_users_collection()
    user_doc = users_col.find_one({"username": user.username})
    if user_doc and pwd_context.verify(user.password, user_doc.get("password", "")):
        return {
            "status": "success",
            "display_name": user_doc.get("display_name", user.username)
        }

    return {"status": "fail"}


@app.post("/save")
def save(data: TextData):
    history_col = get_history_collection()
    history_col.insert_one({
        "username": data.username,
        "text": data.text,
        "summary": data.summary,
        "paraphrase": data.paraphrase,
        "source_name": data.source_name
    })
    return {"status": "saved"}


@app.get("/history/{username}")
def get_history(username: str):
    history_col = get_history_collection()
    documents = list(history_col.find(
        {"username": username},
        {"_id": 1, "text": 1, "summary": 1, "paraphrase": 1, "source_name": 1}
    ))
    return [
        {
            "id": str(doc["_id"]),
            "text": doc.get("text", ""),
            "summary": doc.get("summary", ""),
            "paraphrase": doc.get("paraphrase", ""),
            "source_name": doc.get("source_name", "")
        }
        for doc in documents
    ]


@app.delete("/history/{history_id}")
def delete_history(history_id: str):
    history_col = get_history_collection()
    try:
        history_col.delete_one({"_id": ObjectId(history_id)})
        return {"status": "deleted"}
    except Exception as e:
        return {"status": "error", "message": "Invalid history ID"}