import argparse
import asyncio
import json
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "mysession")

if not API_ID or not API_HASH:
    raise ValueError("ERROR: set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables in .env file!")

parser = argparse.ArgumentParser(description="Telegram guruhdagi faol postlarni tahlil qilish")
parser.add_argument("--session", default=SESSION_NAME, help="Session nomi (default: mysession)")
parser.add_argument("--group", required=True, help="Guruh username, masalan: @djangouzb")
parser.add_argument("--days", type=int, default=7, help="Necha kunlik postlarni olish")
parser.add_argument("--out", default="result.json", help="Natijani JSON faylga yozish")
args = parser.parse_args()


async def main():
    client = TelegramClient(args.session, int(API_ID), API_HASH)
    await client.start()

    print(f"📡 Guruhdan postlar olinmoqda: {args.group}")
    entity = await client.get_entity(args.group)

    limit_date = datetime.now(timezone.utc) - timedelta(days=args.days)
    timezone_name = "Asia/Tashkent"

    # {'2025-10-17': { root_id: {'topic': str, 'messages': set(), 'users': set()} } }
    daily_threads = defaultdict(lambda: defaultdict(lambda: {"topic": "", "messages": set(), "users": set()}))

    async for message in client.iter_messages(entity, limit=2000):
        if message.date < limit_date:
            break

        local_date = message.date.astimezone().strftime("%Y-%m-%d")

        # Root postni aniqlash
        if message.reply_to and message.reply_to.reply_to_msg_id:
            root_id = message.reply_to.reply_to_msg_id
        elif message.reply_to_msg_id:
            root_id = message.reply_to_msg_id
        else:
            root_id = message.id  # agar reply emas — o'zi root bo'ladi

        # Root matnni topish
        if not daily_threads[local_date][root_id]["topic"]:
            if message.text:
                text_preview = message.text.strip().replace("\n", " ")
                if len(text_preview) > 50:
                    text_preview = text_preview[:47] + "..."
                daily_threads[local_date][root_id]["topic"] = text_preview or "(matnsiz post)"
            else:
                daily_threads[local_date][root_id]["topic"] = "(matnsiz post)"

        # Statistikani to'plash
        daily_threads[local_date][root_id]["messages"].add(message.id)
        if message.sender_id:
            daily_threads[local_date][root_id]["users"].add(message.sender_id)

    # Yakuniy JSON format
    result = {"timezone": timezone_name, "days": []}

    for day, posts in sorted(daily_threads.items()):
        threads_list = []
        for root_id, data in posts.items():
            msg_count = len(data["messages"])
            user_count = len(data["users"])
            # Faqat replylar mavjud bo'lgan (ya’ni 1 dan ortiq xabarli) postlarni olish
            if msg_count > 1:
                threads_list.append({
                    "topic": data["topic"],
                    "messages": msg_count,
                    "users": user_count
                })

        # Eng faol postlar bo'yicha tartiblash
        threads_list.sort(key=lambda x: x["messages"], reverse=True)
        result["days"].append({"date": day, "threads": threads_list})

    # JSON faylga yozish
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"✅ Natija '{args.out}' faylga saqlandi.")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
