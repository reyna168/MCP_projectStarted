import pandas as pd
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP Server
mcp = FastMCP("Phone Directory Server")

# 工具：搜尋電話
@mcp.tool()
def search_phone(query: str) -> str:
    """
    搜尋電話簿中的資料
    :param query: 查詢關鍵字
    :return: 查詢結果
    """
    try:
        df = pd.read_excel("phone_directory.xlsx", dtype=str)
        df.columns = [col.strip() for col in df.columns]

        for col in ['姓名', '電話']:
            if col not in df.columns:
                return f"電話表缺少必要欄位：{col}"

        df['電話'] = df['電話'].astype(str)

        mask = (
            df['姓名'].str.contains(query, case=False, na=False) |
            df['電話'].str.contains(query, case=False, na=False)
        )
        results = df[mask]

        if results.empty:
            return "找不到符合查詢條件的資料。"

        response_lines = []
        for _, row in results.iterrows():
            line = f"姓名：{row['姓名']}, 電話：{row['電話']}"
            if '地址' in row and pd.notna(row['地址']):
                line += f", 地址：{row['地址']}"
            if '備註' in row and pd.notna(row['備註']):
                line += f", 備註：{row['備註']}"
            response_lines.append(line)

        return "\n".join(response_lines)

    except Exception as e:
        return f"電話表讀取失敗: {e}"    

# 資源：問候語
@mcp.resource(uri="greeting://{name}",name='greeting',description='用來展示一個資源協議')
def get_greeting(name: str) -> str:
	#訪問處理greeting://{name}資源協議，然後返回
	#為了演示效果，回傳原來呼叫的文字，前面加上Hello,
    return f"Hello, {name}!"
    
# 提示詞：
@mcp.prompt( name='translate', description='進行內容轉英文的prompt')
def translate(message: str) -> str:
    return f'請將下面的內容，轉成英文：\n\n{message}'


# 啟動 MCP Server
if __name__ == "__main__":
    mcp.run()
