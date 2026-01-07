from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import io

app = FastAPI()

API_KEY = os.getenv("API_KEY")

def check_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate")
async def generate(request: Request, data: dict):
    check_api_key(request)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Generated PDF")
    y -= 30

    for k, v in data.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 18

    c.showPage()
    c.save()

    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf"
    )
