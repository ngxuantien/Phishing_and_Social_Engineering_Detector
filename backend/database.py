import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = None

try:
    if url and key:
        supabase = create_client(url, key)
        print("Đã kết nối Supabase thành công.")
    else:
        print("Thiếu SUPABASE_URL hoặc KEY. Chế độ lưu DB sẽ bị tắt.")
except Exception as e:
    print(f"Lỗi kết nối Supabase: {e}")

def save_prediction(text: str, label: str, score: float, ip_address: str = None):
    """Hàm lưu kết quả dự đoán vào bảng 'history' trong Supabase"""
    if not supabase:
        return None
    
    try:
        data = {
            "content": text,
            "prediction": label,
            "confidence": score,
            # Bạn có thể thêm ip_address nếu muốn tracking
        }
        response = supabase.table("history").insert(data).execute()
        return response
    except Exception as e:
        print(f"Lỗi khi lưu vào DB: {e}")
        return None