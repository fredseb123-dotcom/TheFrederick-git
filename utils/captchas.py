"""
Práce s captcha databází
"""

import sqlite3
from PIL import Image, ImageFont, ImageDraw
import random
import string


def write_captcha(member_id: int, captcha: str, fails: int):
    """Zápis dat o captche"""

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO captcha VALUES ('{member_id}', '{captcha}, {fails}')""")
    conn.commit()
    conn.close()


def delete_by_id(member_id: int):
    "Smazání captchi dle ID"

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM captcha WHERE member_id={member_id}""")
    conn.commit()
    conn.close()


def get_captcha(member_id: int):
    """Získání všech dat o danné captchi"""

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM captcha WHERE member_id={member_id}""")
    conn.commit()

    return cursor.fetchone()

def create_captcha(member_id:int):
    text_captcha = random.choices(string.ascii_uppercase + string.digits, k = 10)

    img1 = Image.open("images/captchas/template.png")
    copy_img1 = img1.copy()

    font = ImageFont.truetype("images/captchas/consola.ttf", 75)
    draw = ImageDraw.Draw(copy_img1)
    index_text = 0
    coloring = []

    for i in range(5):
        a = random.randint(0, 1)*255
        coloring.append(a)
        if a == 0:
            coloring.append(255)
        else:
            coloring.append(0)

    correct_text = []
    for num in range(10):
        if coloring[num] == 0:
            correct_text.append(text_captcha[num])
    correct = "".join(correct_text)

    def x_cord():
        return random.randint(30, 470)
    def y_cord():
        return random.randint(30, 170)

    for x in range(5):
        for y in range(2):
            color = coloring[index_text]
            if color == 0:
                draw.line(((x_cord(), y_cord()), (x_cord(), y_cord()), (x_cord(), y_cord()), (x_cord(), y_cord())), fill=(0, 220, 255), width=3)
            draw.text(((x*100)+25, y*100),f"{text_captcha[index_text]}",(color, 255, 255),font=font)
            index_text += 1

    copy_img1.save("images/captchas/captcha.png")
    write_captcha(member_id, correct.lower(), 0)