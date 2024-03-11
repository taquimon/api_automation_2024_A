from dotenv import load_dotenv
import os

load_dotenv()
token_todo = os.getenv("TOKEN")
URL_TODO = "https://api.todoist.com/rest/v2"
HEADERS_TODO = {
    "Authorization": f"Bearer {token_todo}"
}
