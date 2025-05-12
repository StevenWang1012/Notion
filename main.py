from flask import Flask
from notion_client import Client
import os

# 初始化 Notion 客戶端
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = "1ec13521-389b-8012-8793-ee9224e643aa"
notion = Client(auth=NOTION_TOKEN)


# 執行你原本的 Notion 處理邏輯
def process_all_pages():
    response = notion.databases.query(database_id=DATABASE_ID)
    for page in response["results"]:
        props = page["properties"]
        title_raw = props.get("Name", {}).get("title", [])
        title = title_raw[0]["plain_text"] if title_raw else "（無標題）"

        # 統計 Checkbox
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
            progress_text = "✅"
        else:
            progress_text = f"進度 {done}/{total}"

        # 更新頁面屬性
        notion.pages.update(page_id=page["id"],
                            properties={
                                "進度": {
                                    "rich_text": [{
                                        "text": {
                                            "content": progress_text
                                        }
                                    }]
                                }
                            })
        print(f"✅ {title} → {progress_text}")


# Flask Web Server
app = Flask(__name__)


@app.route("/")
def home():
    return "🟢 伺服器正在運行"


@app.route("/run")
def run_job():
    try:
        process_all_pages()
        return "✅ 已成功處理並更新進度"
    except Exception as e:
        return f"❌ 發生錯誤：{e}"


# 啟動伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
