import os
import telebot
from PIL import Image, ImageDraw, ImageFont

# 配置参数
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# 坐标配置 (根据你提供的坐标)
COORDS = {
    "time": (189, 39),
    "battery": (1077, 35),
    "address": (837, 1146),
    "usd_value": (637, 571),
    "amount": (687, 490)
}

def generate_image(amount, address, time_str, battery_level):
    # 1. 加载底图
    base_img = Image.open("assets/base.png").convert("RGBA")
    draw = ImageDraw.Draw(base_img)
    
    # 2. 加载字体 (需确保路径下有字体文件)
    font_main = ImageFont.truetype("fonts/SF-Pro.ttf", 40) 
    font_bold = ImageFont.truetype("fonts/SF-Pro-Bold.ttf", 80)

    # 3. 写入文字 (注意：OKX通常是右对齐或居中，这里先按你提供的坐标左起点写入)
    draw.text(COORDS["time"], time_str, font=font_main, fill=(255, 255, 255))
    draw.text(COORDS["amount"], f"{amount}", font=font_bold, fill=(255, 255, 255))
    draw.text(COORDS["usd_value"], f"~${amount}", font=font_main, fill=(160, 160, 160))
    draw.text(COORDS["address"], address, font=font_main, fill=(255, 255, 255))

    # 4. 叠加电量图
    battery_idx = str(int(int(battery_level)/10))
    battery_icon = Image.open(f"assets/{battery_idx}.png").convert("RGBA")
    base_img.paste(battery_icon, COORDS["battery"], battery_icon)

    out_path = "result.png"
    base_img.save(out_path)
    return out_path

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "请发送参数，格式如下：\n金额|地址|时间|电量\n例如：503|TJ3bjc...HYDp|22:03|80")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        parts = message.text.split('|')
        path = generate_image(parts[0], parts[1], parts[2], parts[3])
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.reply_to(message, f"生成失败，请检查格式。错误: {str(e)}")

bot.polling()