from notion_client import Client
import os
import datetime

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PAGE_ID = "1ec13521389b80a293e0ca47d925c699"  # 替換為你的 Notion 頁面 ID

notion = Client(auth=NOTION_TOKEN)

# 自動執行：啟動main.py時就執行
blocks = notion.blocks.children.list(block_id=PAGE_ID)["results"]
for block in blocks:
    if block["type"] == "paragraph":
        rich_text = block["paragraph"].get("rich_text", [])
        if not rich_text:
            continue

        first_text = rich_text[0]
        plain = first_text.get("plain_text", "")
        if "更新時間" in plain:

            # 取得字體樣式與區塊底色
            annotations = first_text.get("annotations", {})
            block_color = block["paragraph"].get("color", "default")

            # 建立新的 rich_text，套用原本的格式
            updated_rich_text = [{
                "type": "text",
                "text": {
                    "content": f"最後更新時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "annotations": annotations
            }]

            # 執行更新
            notion.blocks.update(
                block_id=block["id"],
                paragraph={
                    "rich_text": updated_rich_text,
                    "color": block_color
                }
            )
            print("🕒 已更新時間段落（保留樣式）")
            break
