from notion_client import Client
import os
import datetime

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PAGE_ID = "1ec13521389b80a293e0ca47d925c699"  # 替換為你的 Notion 頁面 ID

notion = Client(auth=NOTION_TOKEN)

# 自動執行：啟動時就執行
blocks = notion.blocks.children.list(block_id=PAGE_ID)["results"]
for block in blocks:
    if block["type"] == "paragraph":
        text = block["paragraph"]["rich_text"]
        if text and "更新時間" in text[0]["plain_text"]:
            notion.blocks.update(
                block_id=block["id"],
                paragraph={
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": f"最後更新時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    }]
                }
            )
            print("🕒 已更新時間段落")
            break
