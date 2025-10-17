````markdown
# Telegram Muhokama Tahlilchisi

Ushbu loyiha **Telethon** kutubxonasi yordamida Telegram guruhidagi so‘nggi kunlardagi muhokamalarni tahlil qiladi.  
Skript har bir post bo‘yicha nechta xabar yozilganini va nechta foydalanuvchi ishtirok etganini aniqlaydi.

## 🧩 Imkoniyatlar
- Har qanday ochiq Telegram guruhi yoki superguruhdagi xabarlarni olish  
- So‘nggi **N kunlik** muhokamalarni tahlil qilish  
- Eng ko‘p muhokama qilingan postlarni aniqlash  
- Natijani **JSON fayl** ko‘rinishida saqlash

## ⚙️ O‘rnatish
bash
git clone https://github.com/muslimbek77/redteam-task.git
cd redteam-task
python -m venv venv
source venv/bin/activate  # Linux/Mac uchun
venv\Scripts\activate  # Windows uchun
pip install -r requirements.txt
````

## 🔑 .env Fayl Namuna

Telegram hisob ma’lumotlaringizni quyidagicha `.env` faylga yozing:

```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
SESSION_NAME=mysession
```

## 🚀 Ishga tushirish

```bash
python main.py --group @gr_username --days 7 --out result.json
```

## 🧾 Natija Namuna

```json
{
  "timezone": "Asia/Tashkent",
  "days": [
    {
      "date": "2025-10-17",
      "threads": [
        {"topic": "Django ORM haqida savol...", "messages": 26, "users": 9}
      ]
    }
  ]
}
```
