import os
import requests
from main import build_post_text

GRAPH_API_VERSION = "v23.0"

PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")

def post_to_facebook(message: str):
    if not PAGE_ID or not PAGE_TOKEN:
        raise ValueError("Missing FACEBOOK_PAGE_ID or FACEBOOK_PAGE_TOKEN")

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PAGE_ID}/feed"

response = requests.post(
    url,
    data={
        "message": message,
        "access_token": PAGE_TOKEN,
    },
    timeout=30,
)

print("Status code:", response.status_code)
print("Response body:", response.text)

response.raise_for_status()
return response.json()
if __name__ == "__main__":
    post_text = build_post_text()
    print("Posting this message:")
    print(post_text)
    result = post_to_facebook(post_text)
    print("Facebook response:")
    print(result)
