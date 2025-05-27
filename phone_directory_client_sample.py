import asyncio
from mcp import ClientSession, types
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters

async def run_client():
    # 指定 server 啟動指令
    server_params = StdioServerParameters(
        command="python",
        args=["phone_directory_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化連線
            await session.initialize()

            # 呼叫 Tool：搜尋電話
            print("🔍 搜尋電話：")
            result = await session.call_tool("search_phone", {"query": "李"})
            print(result)

            # 呼叫 Resource：問候語
            print("\n👋 問候語：")
            greeting, _ = await session.read_resource("greeting://hihi")
            print(_)
            
            # 呼叫 prompt：提示詞
            print("\n👋 提示詞：")
            prompt = await session.get_prompt('translate',{"message":"how are you?"})
            print(prompt)            

if __name__ == "__main__":
    asyncio.run(run_client())
