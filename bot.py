def generate_screenshot(amount, address, time_str, battery_idx):
    # 1. 加载底图
    base = Image.open("assets/base.jpg").convert("RGBA")
    draw = ImageDraw.Draw(base)
    
    # 2. 字体设置 (建议使用 Inter 或 Roboto)
    font_time = ImageFont.truetype("assets/font_bold.ttf", 34)
    font_amount = ImageFont.truetype("assets/font_bold.ttf", 82)
    font_usd = ImageFont.truetype("assets/font_reg.ttf", 38)
    font_address = ImageFont.truetype("assets/font_reg.ttf", 32)

    # 3. 写入手机时间 (左对齐)
    draw.text((189, 39), time_str, font=font_time, fill=(0, 0, 0))

    # 4. 写入金额 (水平居中)
    # 503 的位置
    draw.text((CENTER_X, 502), amount, font=font_amount, fill=(0, 0, 0), anchor="mm")
    
    # 5. 写入等值 ~$ (水平居中)
    draw.text((CENTER_X, 582), f"~${amount}", font=font_usd, fill=(136, 136, 136), anchor="mm")

    # 6. 地址换行处理
    # 模拟原图：前18位一行，剩下的第二行
    line1 = address[:18]
    line2 = address[18:]
    
    # 地址坐标 (根据你提供的 837, 1146 修正，地址在右侧且右对齐)
    # anchor="ra" 表示右对齐 (Right Aligned)
    addr_x = 837 
    addr_y = 1146 
    
    # 第一行
    draw.text((addr_x, addr_y), line1, font=font_address, fill=(0, 0, 0), anchor="ra")
    # 第二行 (下移 40 像素)
    draw.text((addr_x, addr_y + 40), line2, font=font_address, fill=(0, 0, 0), anchor="ra")

    # 7. 叠加电量图 (坐标 1077, 35)
    try:
        battery_img = Image.open(f"assets/{battery_idx}.png").convert("RGBA")
        base.paste(battery_img, (1077, 35), battery_img)
    except:
        pass

    out_file = "output.png"
    base.save(out_file)
    return out_file