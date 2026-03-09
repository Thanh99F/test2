# --- TƯ DUY ĐIỀU KHIỂN SERVER CLOUD CHUẨN MCP ---
import os
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

# 1. Khởi tạo Server MCP cơ bản
may_chu_soc_nho = Server("SocNhoCloud")

# 2. Định nghĩa công cụ (Tool)
@may_chu_soc_nho.list_tools()
async def danh_sach_cong_cu():
    return [
        {
            "name": "tra_cuu_viet_nam",
            "description": "Ưu tiên tìm kiếm thông tin tại Việt Nam",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "noi_dung": {"type": "string"}
                }
            }
        }
    ]

@may_chu_soc_nho.call_tool()
async def thuc_thi_cong_cu(name, arguments):
    if name == "tra_cuu_viet_nam":
        noi_dung = arguments.get("noi_dung", "")
        return [
            {
                "type": "text",
                "text": f"Sóc Nhỏ đang ưu tiên xử lý dữ liệu Việt Nam cho: {noi_dung}"
            }
        ]

# 3. Thiết lập vận chuyển SSE
van_chuyen_sse = SseServerTransport("/sse")

async def handle_sse(request):
    async with van_chuyen_sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await may_chu_soc_nho.run(read_stream, write_stream, may_chu_soc_nho.create_initialization_options())

# 4. Tạo ứng dụng Starlette (SỬA LỖI TẠI ĐÂY)
# Giải thích: Đổi Mount thành Route để tương thích với endpoint của SSE
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=van_chuyen_sse.handle_post_message, methods=["POST"]),
    ]
)

if __name__ == "__main__":
    # Lấy cổng PORT từ Render (mặc định 10000 hoặc 8000)
    cong_port = int(os.environ.get("PORT", 8000))
    # Chạy uvicorn - người gác cổng cho Sóc Nhỏ
    uvicorn.run(app, host="0.0.0.0", port=cong_port)


