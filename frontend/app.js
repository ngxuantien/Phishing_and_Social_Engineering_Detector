// const API_URL = "http://127.0.0.1:8000/api/detect";
const API_URL = "https://nxtcute-doan-tn-backend.hf.space/api/detect";

document.addEventListener("DOMContentLoaded", () => {
    const checkBtn = document.getElementById("checkBtn");
    const inputText = document.getElementById("inputText");

    // Gắn sự kiện click cho nút bấm
    checkBtn.addEventListener("click", checkText);

    // Gắn sự kiện nhấn Enter để kiểm tra luôn
    inputText.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Ngăn xuống dòng
            checkText();
        }
    });
});

async function checkText() {
    const input = document.getElementById("inputText").value.trim();
    const resultDiv = document.getElementById("result");
    const mainRes = document.getElementById("mainRes");
    const subRes = document.getElementById("subRes");
    const checkBtn = document.getElementById("checkBtn");

    // Reset giao diện
    resultDiv.className = "result";
    mainRes.textContent = "";
    subRes.textContent = "";

    // Validate đầu vào
    if (!input) {
        alert("Vui lòng nhập văn bản hoặc URL để kiểm tra!");
        return;
    }

    // Hiệu ứng nút bấm đang xử lý
    const originalBtnText = checkBtn.innerHTML; // Lưu nội dung nút cũ
    checkBtn.disabled = true;
    checkBtn.style.opacity = "0.7";
    checkBtn.innerHTML = "Đang phân tích...";

    try {
        // 4. Gọi API Backend
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (response.ok) {
            // 5. Xử lý kết quả thành công
            let className = "";
            let icon = "";

            // Logic kiểm tra nhãn trả về (Phishing hay An toàn)
            if (data.label.includes("ĐỘC HẠI") || data.label.includes("PHISHING")) {
                className = "phishing";
                icon = "⚠️";
            } else {
                className = "safe";
                icon = "✅";
            }

            // Hiển thị ra màn hình
            mainRes.innerHTML = `${icon} <strong>${data.label}</strong> <br> (Độ tin cậy: ${(data.score * 100).toFixed(2)}%)`;
            subRes.textContent = data.message; // Lời khuyên từ backend

            resultDiv.classList.add(className, "show");
        } else {
            // Xử lý lỗi từ server trả về (400, 500)
            throw new Error(data.detail || "Lỗi không xác định từ server");
        }
    } catch (err) {
        // 6. Xử lý lỗi kết nối
        mainRes.innerHTML = `<strong>Lỗi kết nối</strong>`;
        subRes.textContent = `Không thể gọi đến Backend. Hãy chắc chắn rằng file main.py đang chạy. (${err.message})`;
        resultDiv.classList.add("phishing", "show"); // Dùng style đỏ để cảnh báo
        console.error("Lỗi:", err);
    } finally {
        // 7. Khôi phục trạng thái nút bấm
        checkBtn.disabled = false;
        checkBtn.style.opacity = "1";
        checkBtn.innerHTML = originalBtnText;
    }
}