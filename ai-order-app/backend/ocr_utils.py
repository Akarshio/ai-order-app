import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text from image or PDF file."""
    if filename.lower().endswith(".pdf"):
        pages = convert_from_bytes(file_bytes)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        return text
    else:
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)
