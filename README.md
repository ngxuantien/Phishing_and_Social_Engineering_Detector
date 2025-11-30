🛡️ Phishing & Social Engineering Detection System
Đồ án Tốt nghiệp: Hệ thống Ứng dụng Large Language Models - LLMs trong phát hiện tấn công Lừa đảo (Phishing) và Kỹ nghệ xã hội (Social Engineering)

Giới thiệu: Dự án này là một giải pháp an ninh mạng tích hợp, giúp người dùng phát hiện các mối đe dọa từ tin nhắn văn bản (SMS, Email, Chat) và đường dẫn (URL) độc hại. Hệ thống sử dụng mô hình học sâu chuyên biệt (Fine-tuned XLM-R) để đạt độ chính xác cao nhất và giảm thiểu báo động giả.

Tính năng nổi bật: 
  Sử dụng mô hình XLM-R (đã fine-tune cho tiếng Việt) để phân loại nhanh văn bản với độ trễ thấp.
  Trả về nhãn "Độc hại/An toàn" nhanh chóng.
  Lưu trữ & Thống kê: Tích hợp Supabase để lưu trữ lịch sử nhằm tra cứu, phục vụ việc tái huấn luyện mô hình sau này.
  Modern Deployment: Kiến trúc tách biệt (Decoupled) với Backend chạy trên Docker (Hugging Face Spaces) và Frontend trên Vercel.

Hệ thống hoạt động dựa trên luồng xử lý dữ liệu thông minh:
  Input: Người dùng nhập văn bản hoặc URL.
  Preprocessor: Xác định định dạng đầu vào (Text hay URL).
  XLM-R: Phân tích ngữ nghĩa văn bản.
  Output: Kết quả cuối cùng.

Công nghệ sử dụng (Tech Stack):
  Backend (API & AI Core)
  Language: Python 3.10
  Framework: FastAPI (High performance async API)

AI/ML:
  transformers (Hugging Face)
  pytorch (CPU Optimized for Deployment)
  Database: Supabase (PostgreSQL)
  Containerization: Docker

Frontend (Client)
  Core: HTML5, CSS3, JavaScript
  Features: Hiệu ứng Loading, CSS Animations, Mobile-first design.

Deployment (DevOps)
  Backend: Hugging Face Spaces (Docker SDK).
  Frontend: Vercel.
  Source Control: GitHub.

Cài đặt & Chạy Local (Installation)
1. Clone dự án
  git clone [https://github.com/ngxuantien/Phishing_and_Social_Engineering_Detector.git](https://github.com/ngxuantien/Phishing_and_Social_Engineering_Detector.git)
  cd Phishing_and_Social_Engineering_Detector

2. Cấu hình Backend
  Di chuyển vào thư mục backend và tạo môi trường ảo:
    cd backend
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
  
  Cài đặt thư viện:
    pip install -r requirements.txt
    Tạo file .env và cấu hình các biến môi trường:
    MODEL_ID=nxtcute/xlm-r-finetuned-vi  # Link repo trên Hugging Face
    DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx     # API Key của DeepSeek
    SUPABASE_URL=[https://xxxx.supabase.co](https://xxxx.supabase.co)
    SUPABASE_KEY=eyJh...
  
  Chạy Server:
    uvicorn main:app --reload
    Server sẽ chạy tại: http://127.0.0.1:8000

3. Cấu hình Frontend
  Mở file frontend/app.js và cập nhật API Endpoint:
    const API_URL = "[http://127.0.0.1:8000/api/detect](http://127.0.0.1:8000/api/detect)"; // Nếu chạy local
    [//link Cloud nếu đã deploy](https://phishing-and-social-engineering-det-two.vercel.app/)
    Mở file frontend/index.html trên trình duyệt để trải nghiệm.
  
  Docker Deployment
    Dự án đã được tối ưu hóa Dockerfile để deploy trên các nền tảng giới hạn tài nguyên (như Hugging Face Spaces Free Tier).
    # Build Docker Image
    docker build -t phishing-api .
    # Run Container
    docker run -p 7860:7860 --env-file .env phishing-api

API Documentation
  POST /api/detect
  Request Body:
  {
    "text": "Tài khoản của bạn bị khóa. Truy cập bank-verify-vn.com để mở lại."
  }
  
  Response:
  {
    "status": "success",
    "label": "ĐỘC HẠI (PHISHING)",
    "score": 0.98,
    "message": "phát hiện mối đe dọa kỹ thuật/lừa đảo."
  }
