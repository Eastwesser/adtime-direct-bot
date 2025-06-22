# AdTime Direct (tg bot)

Use our Telegram bot to create orders for leather accessories, vinyl stickers, and gift cards!

## Features

**Art with Kandinsky**: Convert text into images with Kandinsky. You may draw any picture you like, 
except violent or restricted ones.

## Installation

To install the necessary dependencies, here are the required libraries:

```plaintext
aiogram==3.5.0
python-dotenv==1.0.1
pydantic-settings==2.2.1
aiohttp~=3.9.0
requests==2.32.4
psutil==5.9.8
```
## .env Sample
For tokens and other data use .env:

```commandline
BOT_TOKEN=your_telegram_bot_token
FUSION_BRAIN_TOKEN=your_fusion_brain_token
FB_KEY=your_fusion_brain_key
```

# Run:

```bash
python main.py

# or using webhook

python webhook-server/webhook.py
```

Feel free to interact with AdTime bot and explore its current functionalities.
Stay tuned for updates and new features as we continue to enhance its capabilities! 🚀