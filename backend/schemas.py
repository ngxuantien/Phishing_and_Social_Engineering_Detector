from pydantic import BaseModel
from typing import Optional

# Dữ liệu Frontend gửi lên
class CheckRequest(BaseModel):
    text: str

# Dữ liệu Backend trả về
class CheckResponse(BaseModel):
    status: str          # "success" hoặc "error"
    input_text: str
    label: str           # "AN TOÀN" hoặc "ĐỘC HẠI"
    score: float         # 0.99
    message: str         # Lời khuyên cho người dùng