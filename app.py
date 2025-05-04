from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.relational_database_storage import RelationalDatabaseStorage
from modules.key_value_storage import KeyValueStorage
from modules.object_storage import ObjectStorage
from modules.vector_storeage import VectorStorage
from modules.chatbot import Chatbot
from modules.utils import Utils
import pymysql, uuid, os, tempfile

app = FastAPI()

# DB config
DB_CONFIG = {
    'host': 'chatbot-db.cipyg4o8m0fb.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': '12345678',
    'database': 'chatbot-db'
}

S3_BUCKET = "big-data-analytics-001"

# Create database & tables (if not already done)
RelationalDatabaseStorage.setup_chatbot_db(DB_CONFIG)

# ----------- Pydantic Models ------------
class SignUpRequest(BaseModel):
    user_id: str
    name: str
    email: str

class SignInRequest(BaseModel):
    user_id: str


# ----------- API Endpoints ------------

@app.post("/signup")
def signup(user: SignUpRequest):
    conn = RelationalDatabaseStorage.connect_to_db(DB_CONFIG)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, name, email) VALUES (%s, %s, %s)",
            (user.user_id, user.name, user.email)
        )
        conn.commit()
        return {"message": "✅ User signed up successfully."}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="❌ User ID already exists.")
    finally:
        cursor.close()
        conn.close()

@app.post("/signin")
def signin(user: SignInRequest):
    conn = RelationalDatabaseStorage.connect_to_db(DB_CONFIG)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user.user_id,))
        result = cursor.fetchone()
        if result:
            session_id = str(uuid.uuid4())  # generate a unique session ID
            cursor.execute(
                "INSERT INTO sessions (session_id, user_id) VALUES (%s, %s)",
                (session_id, user.user_id)
            )
            conn.commit()
            return {"message": "✅ Sign-in successful", "session_id": session_id}
        else:
            raise HTTPException(status_code=404, detail="❌ User not found.")
    finally:
        cursor.close()
        conn.close()

@app.post("/chat")
async def chat(
    user_id: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None)
):
    try:
        # Step 1: Save file to S3 (if uploaded)
        if file:
            folder_name = f"{user_id}/uploads"
            ObjectStorage.create_s3_folder(S3_BUCKET, folder_name)

            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # Upload to S3
            ObjectStorage.upload_file_to_s3(S3_BUCKET, folder_name, tmp_path)

            docs = Utils.get_text_from_files(tmp_path)

            doc_chunks = Utils.split_text_to_chunks(docs)

            VectorStore = VectorStorage.load_vectorstore()

            VectorStore = VectorStorage.insert_chunks_to_vectordb(doc_chunks)

            retriver = VectorStore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 100})

            # compression_retriever = VectorStorage.get_rerank_retriever(retriver)

            bot_response, docs = Chatbot.rag_response(retriver, message)

            KeyValueStorage.insert_conversation_log(user_id, message, bot_response)

            os.remove(tmp_path)
            Utils.delete_folder("vector_store")

            return JSONResponse(content={
                "user_id": user_id,
                "message": message,
                "bot_response": bot_response
            })
        else:
            bot_response = Chatbot.simple_response(message)

            return JSONResponse(content={
                "user_id": user_id,
                "message": message,
                "bot_response": bot_response,
            })

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
