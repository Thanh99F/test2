# --- TƯ DUY ĐIỀU KHIỂN SERVER CLOUD CHUẨN MCP ---
import os
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request

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
    # Lý thuyết: Duy trì luồng đọc/ghi dữ liệu liên tục cho SSE
    async with van_chuyen_sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await may_chu_soc_nho.run(read_stream, write_stream, may_chu_soc_nho.create_initialization_options())

async def handle_messages(request: Request):
    # GIẢI PHÁP: Bọc hàm handle_post_message để truyền đủ scope, receive, send
    # Đây là nơi sửa lỗi "TypeError: missing 2 required positional arguments"
    return await van_chuyen_sse.handle_post_message(
        request.scope,
        request.receive,
        request.send
    )

# 4. Tạo ứng dụng Starlette
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        # Thay đổi từ truyền hàm trực tiếp sang dùng hàm bọc (Wrapper)
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]
)

if __name__ == "__main__":
    cong_port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=cong_port)
