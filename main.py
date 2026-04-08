from config import NOTION_TOKEN, PAGE_ID_MEETING_1
from notion_client import Client
import datetime
import pytz

def run_update():
    notion = Client(auth=NOTION_TOKEN)

    # 取得台灣時間（UTC+8）
    taiwan_tz = pytz.timezone("Asia/Taipei")
    now = datetime.datetime.now(taiwan_tz)
    new_text = f"最後更新時間：{now.strftime('%Y-%m-%d %H:%M')}"

    try:
        # 抓取頁面區塊
        blocks = notion.blocks.children.list(block_id=PAGE_ID_MEETING_1)["results"]

        for block in blocks:
            if block["type"] == "paragraph":
                rich_text = block["paragraph"].get("rich_text", [])
                if not rich_text:
                    continue

                first_text = rich_text[0]
                if "更新時間" in first_text.get("plain_text", ""):
                    # 保留樣式
                    annotations = first_text.get("annotations", {})
                    block_color = block["paragraph"].get("color", "default")

                    updated_rich_text = [{
                        "type": "text",
                        "text": {"content": new_text},
                        "annotations": annotations
                    }]

                    notion.blocks.update(
                        block_id=block["id"],
                        paragraph={
                            "rich_text": updated_rich_text,
                            "color": block_color
                        }
                    )
                    print(f"🕒 {new_text} - 已同步至 Notion")
                    return
    except Exception as e:
        print(f"❌ 更新時間段落失敗: {e}")

if __name__ == "__main__":
    run_update()
