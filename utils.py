import requests


def send_telegram_message(bot_token: str, admin_id: int, message: str):
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": admin_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(base_url, data=payload)
    return response.json()


def create_telegram_message(item: dict):
    title = item["title"]
    description = item["missionDoc"]["content"][0]["content"][0]["text"]
    url = "https://app.layer3.xyz/quests/" + item["slug"] + "?ref=goftok.eth"
    return f"<b>{title}</b>\n{description}\n<a href='{url}'>Click</a>"
