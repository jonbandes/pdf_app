from fastapi import FastAPI, Request, Header, Query
from routes.c_pdf import generate_pdf_generic_logic

app = FastAPI()

@app.post("/generate_pdf")
async def generate_pdf_generic(request: Request, api_key: str = Header(None), idMember: int = Query(...,), idVerification: str = Query(...,)):
    return generate_pdf_generic_logic(api_key, idMember, idVerification)
