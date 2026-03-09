# --- TƯ DUY ĐIỀU KHIỂN SERVER CLOUD CHUẨN MCP ---
import os
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount

# 1. Khởi tạo Server MCP cơ bản
may_chu_soc_nho = Server("SocNhoCloud")

# 2. Định nghĩa công cụ (Tool) - Giải thích: Khai báo để AI biết nó có kỹ năng gì
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
        # Logic: AI sẽ nhận kết quả này để trả lời bạn
        return [
            {
                "type": "text",
                "text": f"Sóc Nhỏ đang ưu tiên xử lý dữ liệu Việt Nam cho: {noi_dung}"
            }
        ]

# 3. Thiết lập vận chuyển SSE (Server-Sent Events)
van_chuyen_sse = SseServerTransport("/sse")

async def handle_sse(request):
    # Giải thích: Mở đường ống dẫn dữ liệu liên tục
    async with van_chuyen_sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await may_chu_soc_nho.run(read_stream, write_stream, may_chu_soc_nho.create_initialization_options())

# 4. Tạo ứng dụng Starlette để Render giữ máy chủ luôn sống
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", endpoint=van_chuyen_sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    # Lấy cổng PORT từ Render cấp phát
    cong_port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=cong_port)


