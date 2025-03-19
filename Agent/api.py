from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
import shutil
import os

from database import Database
from chain import Chain

# Initialize FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str

# Directory to store uploaded files
UPLOAD_DIR = "Uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov"}

# Endpoint to handle chat input
@app.post("/chat")
async def chat(
    chat_data: ChatRequest = Depends(),
    text: Optional[str] = None,
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None)
):
    response_data = {
        "session_id": chat_data.session_id, 
        "text": text,
        "files": []
    }

    video_path = None
    attachments = []
    approved = True

    # Validate and Save Image
    if image:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG allowed.")
        
        image_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        response_data["files"].append({"type": "image", "path": image_path})
        attachments.append(image_path)

    # Validate and Save Video
    if video:
        ext = os.path.splitext(video.filename)[1].lower()
        if ext not in VIDEO_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid video format. Only MP4, AVI, and MOV allowed.")
        
        video_path = f"{UPLOAD_DIR}/{video.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        response_data["files"].append({"type": "video", "path": video_path})

    print(f"Received: session_id={chat_data.session_id}, text={text}")
    print(f"Image: {image.filename if image else 'No image'}")
    print(f"Video: {video.filename if video else 'No video'}")

    chain_instance = Chain("Images/reference.jpg")
    chain_output = chain_instance.chains(attachments, video_path)

    if isinstance(chain_output, tuple):
        approved, attachments = chain_output
        response_data["approved"] = approved
    elif isinstance(chain_output, list):
        attachments = chain_output

    if approved:
        db = Database(chat_data.session_id)
        previous_messages = db.get_messages()
        attachment_text = "\n-------------\n".join(attachments)
        attachment_text = "Data from Attachments provided by the User:\n\n" + attachment_text if attachment_text else ""
        text = text if text else ""
        text += attachment_text
        agent_response = chain_instance.agent(previous_messages, text, db)
        response_data["agent_response"] = agent_response
        db.close_connection()
    
    else:
        response_data["agent_response"] = "Face Not Matched!"
    

    return {"message": "Chat data received", "data": response_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", reload=True)
