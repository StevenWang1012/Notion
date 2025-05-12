from config import NOTION_TOKEN, PAGE_ID_MEETING_1
from notion_client import Client
import datetime
import pytz

notion = Client(auth=NOTION_TOKEN)

# 取得台灣時間（UTC+8），格式：不含秒
taiwan_tz = pytz.timezone("Asia/Taipei")
now = datetime.datetime.now(taiwan_tz)
new_text = f"最後更新時間：{now.strftime('%Y-%m-%d %H:%M')}"

# 抓取頁面區塊
blocks = notion.blocks.children.list(block_id=PAGE_ID_MEETING_1)["results"]

for block in blocks:
    if block["type"] == "paragraph":
        rich_text = block["paragraph"].get("rich_text", [])
        if not rich_text:
            continue

        first_text = rich_text[0]
        if "更新時間" in first_text.get("plain_text", ""):
            # 保留樣式（字體樣式 + 區塊底色）
            annotations = first_text.get("annotations", {})
            block_color = block["paragraph"].get("color", "default")

            updated_rich_text = [{
                "type": "text",
                "text": {
                    "content": new_text
                },
                "annotations": annotations
            }]

            notion.blocks.update(
                block_id=block["id"],
                paragraph={
                    "rich_text": updated_rich_text,
                    "color": block_color
                }
            )
            print("🕒 已更新時間段落（保留樣式）")
            break
