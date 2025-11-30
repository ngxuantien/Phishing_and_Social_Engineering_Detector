# 1. Dùng bản python-slim (rất nhẹ, giảm bớt vài trăm MB hệ điều hành thừa)
FROM python:3.10-slim

# 2. Thiết lập User (Bắt buộc cho HF Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# 3. Cài đặt các gói hệ thống tối thiểu (nếu cần cho transformers)
# Chuyển về root tạm thời để cài
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
USER user

# 4. 🔥 BƯỚC QUAN TRỌNG NHẤT: Cài PyTorch bản CPU (Siêu nhẹ)
# Tách riêng bước này ra để Docker cache lại, không phải tải lại mỗi lần sửa code
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 5. Copy requirements và cài các thư viện còn lại
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 6. Copy toàn bộ code
COPY --chown=user . .

# 7. Mở port 7860
EXPOSE 7860

# 8. Chạy server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]