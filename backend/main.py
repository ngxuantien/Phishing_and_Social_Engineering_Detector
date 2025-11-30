import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from dotenv import load_dotenv

from schemas import CheckRequest, CheckResponse
from database import save_prediction 

classifier = None
MODEL_PATH = os.getenv("MODEL_ID", "./xlmr-finetuned")

load_dotenv()

app = FastAPI(title="Phishing Detection API", version="1.0.0")

# CẤU HÌNH CORS CHO FRONTEND
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KHỞI TẠO MODEL

@app.on_event("startup")
def load_model():
    global classifier
    
    print("⏳ Đang tải mô hình XLM-R...")
    try:
        classifier = pipeline("text-classification", model=MODEL_PATH, tokenizer=MODEL_PATH, device=-1)
        print(f"Mô hình đã tải xong từ: {MODEL_PATH}")
    except Exception as e:
        print(f"Lỗi nghiêm trọng: Không tải được mô hình XLM-R. {e}")

# ENDPOINT (/api/detect) 

@app.post("/api/detect", response_model=CheckResponse)
async def detect_phishing(request: CheckRequest, api_request: Request):
    if not classifier:
        raise HTTPException(status_code=503, detail="Mô hình chưa sẵn sàng.")
    
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Vui lòng nhập văn bản.")

    # Dự đoán bằng XLM-R thuần túy
    try:
        # XLM-R trả về list dict, ví dụ: [{'label': 'LABEL_1', 'score': 0.99}]
        res = classifier(text)[0]
        raw_lbl = res['label']
        score = round(res['score'], 4)
        
        # Mapping nhãn (Cần khớp với lúc train model)
        # Ví dụ: LABEL_1 = Phishing, LABEL_0 = Normal
        if raw_lbl in ["LABEL_1", "PHISHING", "1"]:
            label_vn = "ĐỘC HẠI (PHISHING)"
            msg = "CẢNH BÁO: Mô hình phát hiện dấu hiệu lừa đảo. Hãy thận trọng khi tương tác với nội dung này."
        else:
            label_vn = "AN TOÀN"
            msg = "Nội dung này có vẻ an toàn. Tuy nhiên hãy luôn cảnh giác."

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý mô hình: {str(e)}")

    # Lưu kết quả vào Database
    client_ip = api_request.client.host
    save_prediction(text, label_vn, score, client_ip) 

    return {
        "status": "success",
        "input_text": text,
        "label": label_vn,
        "score": score,
        "message": msg,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)