# --- TƯ DUY ĐIỀU KHIỂN SERVER CLOUD ---
from mcp.server.fastmcp import FastMCP
import uvicorn

# Khởi tạo Sóc Nhỏ với chuẩn SSE để chạy trên Web
app = FastMCP("SocNhoCloud")

@app.tool()
def tra_cuu_thong_tin_viet_nam(cau_hoi: str) -> str:
    """Công cụ giúp Sóc Nhỏ hiểu biết về Việt Nam"""
    # Giải thích: Đây là nơi bạn 'nạp' kiến thức riêng cho Robot
    if "thời tiết" in cau_hoi.lower():
        return "Hãy ưu tiên dự báo thời tiết tại các tỉnh thành Việt Nam từ nguồn KTTV."
    if "địa chỉ" in cau_hoi.lower():
        return "Đây là một địa điểm nằm tại Việt Nam, hãy tra cứu trên bản đồ địa phương."
    
    return f"Đang tối ưu hóa tìm kiếm cho nội dung: {cau_hoi} tại Việt Nam."

if __name__ == "__main__":
    # Chạy dưới dạng máy chủ Web chuyên nghiệp trên cổng 8000
    uvicorn.run(app.as_asgi(), host="0.0.0.0", port=8000)