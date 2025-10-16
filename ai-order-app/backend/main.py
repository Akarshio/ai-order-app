from fastapi import FastAPI, UploadFile
from openai import OpenAI
from dotenv import load_dotenv
import os
import io
from ocr_utils import extract_text_from_file

load_dotenv()
app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
