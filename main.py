from config import NOTION_TOKEN, DATABASE_ID_MEETING_1
from notion_client import Client
import update_timestamp

notion = Client(auth=NOTION_TOKEN)

def process_all_pages():
    print("🚀 開始掃描資料庫進度...")
    try:
        response = notion.databases.query(database_id=DATABASE_ID_MEETING_1)
        
        for page in response["results"]:
            props = page["properties"]
            title_raw = props.get("Name", {}).get("title", [])
            title = title_raw[0]["plain_text"] if title_raw else "（無標題）"

            # 統計 Checkbox 狀態
            plain_text = ""
            for block in notion.blocks.children.list(page["id"])["results"]:
                if block["type"] == "to_do":
                    emoji = "✅" if block["to_do"]["checked"] else "⬜️"
                    plain_text += emoji

            total = plain_text.count("✅") + plain_text.count("⬜️")
            done = plain_text.count("✅")

            if total == 0:
                progress_text = ""
            elif done == total:
                progress_text = "✅ 已完成"
            else:
                progress_text = f"進度 {done}/{total}"

            # 更新頁面屬性
            notion.pages.update(
                page_id=page["id"],
                properties={
                    "進度": {
                        "rich_text": [{"text": {"content": progress_text}}]
                    }
                }
            )
            print(f"🔹 {title} → {progress_text}")
            
    except Exception as e:
        print(f"❌ 處理資料庫時發生錯誤: {e}")

if __name__ == "__main__":
    # 1. 先更新全域頁面的時間戳
    update_timestamp.run_update()
    
    # 2. 再處理資料庫內各分頁進度
    process_all_pages()
    print("🏁 所有任務處理完畢")
