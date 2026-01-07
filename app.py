from fastapi import FastAPI
from fastapi.responses import Response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate")
def generate(data: dict):
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

    pdf_bytes = buffer.getvalue()
    return Response(content=pdf_bytes, media_type="application/pdf")
