
from fastapi import FastAPI, UploadFile
from openai import OpenAI
import os
from ocr_utils import extract_text_from_file
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
# Use GitHub Secret or environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables! Please add it to your .env file.")

client = OpenAI(api_key=api_key)

@app.get("/")
def root():
    return {"message": "AI Ticket Extraction API is running!"}

@app.post("/extract")
async def extract_ticket(file: UploadFile):
    file_bytes = await file.read()
    extracted_text = extract_text_from_file(file_bytes, file.filename)

    prompt = f"""
    Extract structured railway ticket details from this text:
    {extracted_text}

    Return JSON format with:
    - train_name
    - train_number
    - source
    - destination
    - date
    - time
    - pnr
    - passenger_details
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {"data": response.output[0].content[0].text}
