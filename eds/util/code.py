from random import randint,choice
from PIL import Image,ImageDraw,ImageFont
from io import StringIO
import  io
from string import printable

class Code:

    def create_validate_code(self):
        font_color = (randint(150, 200), randint(0, 150), randint(0, 150))
        line_color = (randint(0, 150), randint(0, 150), randint(150, 200))
        point_color = (randint(0, 150), randint(50, 150), randint(150, 200))

        # 设置验证码的宽与高
        width, height = 100, 34
        image = Image.new("RGB", (width, height), (200, 200, 200))
        font = ImageFont.truetype('arial.ttf', 24)
        draw = ImageDraw.Draw(image)

        # 生成验证码
        text = "".join([choice(printable[:62]) for i in range(4)])
        # 把验证码写在画布上
        draw.text((10, 10), text, font=font, fill=font_color)
        # 绘制干扰线
        for i in range(0, 5):
            draw.line(((randint(0, width), randint(0, height)),
                       (randint(0, width), randint(0, height))),
                      fill=line_color, width=2)

        # 绘制点
        for i in range(randint(100, 1000)):
            draw.point((randint(0, width), randint(0, height)), fill=point_color)
        # 输出
        stream = io.BytesIO()
        image.save(stream, "png")

        return text, stream.getvalue()

    def create_code(self):
        text = "".join([choice(printable[:62]) for i in range(4)])
        return text

code=Code()