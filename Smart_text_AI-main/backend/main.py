from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services.qna import router as qna_router
from services.translate_text import router as translate_router
from services.extract_text import router as extract_router
from services.summarize_text import router as summarize_router
from services.extract_images import router as images_router
from services.transliteration import router as transliteration_router

app = FastAPI(title="AI Document Processor API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(qna_router, prefix="/api", tags=["QnA"])
app.include_router(translate_router, prefix="/api", tags=["Translation"])
app.include_router(extract_router, prefix="/api", tags=["Text Extraction"])
app.include_router(summarize_router, prefix="/api", tags=["Summarization"])
app.include_router(images_router, prefix="/api", tags=["Image Extraction"])
app.include_router(transliteration_router, prefix="/api", tags=["Transliteration"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Remove these lines if they exist
@app.post("/api/translate-text/")
async def translate_text_endpoint(
    file: UploadFile = File(None),
    text: str = Form(None),
    target_language: str = Form(...),
):
    try:
        result = await translate_text_service(text, file, target_language)
        return {"translated_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
