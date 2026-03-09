# --- TƯ DUY ĐIỀU KHIỂN SERVER CLOUD ---
from mcp.server.fastmcp import FastMCP

# Khởi tạo Sóc Nhỏ
app = FastMCP("SocNhoCloud")

@app.tool()
def tra_cuu_thong_tin_viet_nam(cau_hoi: str) -> str:
    """Công cụ giúp Sóc Nhỏ hiểu biết về Việt Nam"""
    # Giải thích: Logic xử lý yêu cầu từ Robot
    if "thời tiết" in cau_hoi.lower():
        return "Dữ liệu thời tiết tại Việt Nam đang được ưu tiên tra cứu."
    if "địa chỉ" in cau_hoi.lower():
        return "Dữ liệu địa chỉ tại các tỉnh thành Việt Nam đang được ưu tiên tra cứu."
    if "âm nhạc" in cau_hoi.lower():
        return "Dữ liệu âm nhạc tại Việt Nam đang được ưu tiên tra cứu."
    return f"Sóc Nhỏ đang tìm hiểu về: {cau_hoi}"

if __name__ == "__main__":
    # GIẢI PHÁP: Sử dụng phương thức run() mặc định của FastMCP.
    # Thư viện sẽ tự động nhận diện môi trường và chạy SSE server.
    app.run()
