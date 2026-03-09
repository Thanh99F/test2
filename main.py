# --- TƯ DUY ĐIỀU KHIỂN SERVER CLOUD 24/7 ---
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
import os
import uvicorn

# 1. Khởi tạo Sóc Nhỏ
mcp = FastMCP("SocNhoCloud")

@mcp.tool()
def tra_cuu_viet_nam(noi_dung: str) -> str:
    """Công cụ giúp Sóc Nhỏ ưu tiên thông tin tại Việt Nam"""
    return f"Sóc Nhỏ đang xử lý: '{noi_dung}' với dữ liệu ưu tiên tại Việt Nam."

# 2. Tạo ứng dụng Web để Render không đóng lại
# Giải thích: Render cấp một cổng 'PORT' ngẫu nhiên, ta phải lấy đúng cổng đó.
app = Starlette(
    routes=[
        Mount("/sse", mcp.as_asgi()), # Lắng nghe tại đường dẫn /sse
    ]
)

if __name__ == "__main__":
    # Lấy cổng từ môi trường Render, mặc định là 8000 nếu chạy máy lẻ
    cong_ket_noi = int(os.environ.get("PORT", 8000))
    
    # Chạy Web Server chuyên nghiệp
    uvicorn.run(app, host="0.0.0.0", port=cong_ket_noi)
