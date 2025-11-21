import httpx
import io
from pypdf import PdfReader

async def extract_text_from_pdf(pdf_url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(pdf_url)
        response.raise_for_status()
        
    pdf_file = io.BytesIO(response.content)
    reader = PdfReader(pdf_file)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    return text
