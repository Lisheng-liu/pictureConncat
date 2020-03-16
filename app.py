import random

from PIL import ImageDraw, ImageFont
from flask import Flask, Response, request, render_template
from werkzeug.utils import secure_filename
import os
import PIL.Image as Image
import time
import stat

app = Flask(__name__)

# 设置图片保存文件夹
# UPLOAD_FOLDER = 'photo'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = "C:/Users/19508/Desktop/pictureConcatTest/"

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


# IMAGES_PATH = 'C:\\Users\\19508\\Desktop\\pictureConcat\\'  # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
IMAGE_SIZE = 256  # 每张小图片的大小
IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 2  # 图片间隔，也就是合并成一张图后，一共有几列


# IMAGE_SAVE_PATH = 'C:\\Users\\19508\\Desktop\\pictureConcat\\final.jpg'  # 图片转换后的地址

# 定义图像拼接函数
def image_compose(IMAGES_PATH):
    # 获取图片集地址下的所有图片名称
    IMAGE_SAVE_PATH = IMAGES_PATH + '/' + 'final.jpg'
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]

    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
        raise ValueError("合成图片的参数和要求的数量不能匹配！")
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + '/' + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


def concatText(info):
    illegal_action = "违反禁止标线"
    illegal_code = "1345"
    security_code = str(getRandomSet(18)).upper()
    illegal_text = "监测点信息：" + info['monitorPlace'] + "  " + "抓拍时间：" + info['cameraTime'] + " \n" \
                   + "车牌号码：" + info['carNum'] + "  " + "违法行为：" + illegal_action + " \n" \
                   + "违法代码：" + illegal_code + "    " + "防伪码：" + security_code
    return illegal_text


def getRandomSet(bits):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set


# 上传图片
@app.route("/photo/upload", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        # file = request.files['file']
        files = request.files
        INFO = ('file', 'carNum', 'monitorPlace', 'cameraTime')
        form_data = request.form.to_dict()
        # form_data.get("")

        infos = []
        for i in range(4):
            index = i + 1
            file = files[INFO[0] + str(index)]
            print(file.filename)
            img = Image.open(file)
            info = {INFO[0]: img, INFO[1]: form_data.get(INFO[1]),
                    INFO[2]: form_data.get(INFO[2]),
                    INFO[3]: form_data.get(INFO[3] + str(index))}
            infos.append(info)

        TEXT_HEIGHT = 180  # 文本框高度
        pic_width = infos[0][INFO[0]].size[0]
        pic_height = infos[0][INFO[0]].size[1]
        width = 2 * pic_width  # 上传的4张图片的宽度和高度需一致
        height = pic_height * 2 + TEXT_HEIGHT * 2
        pj = Image.new("RGB", [width, height], "white")

        img_1 = infos[0][INFO[0]]
        pj.paste(img_1, (0, 0, pic_width, pic_height))
        img_1_1 = drawTextBlock(img_1, TEXT_HEIGHT, infos[0])
        pj.paste(img_1_1, (0, pic_height, pic_width, pic_height + TEXT_HEIGHT))

        img_2 = infos[1][INFO[0]]
        pj.paste(img_2, (pic_width, 0, 2 * pic_width, pic_height))
        img_2_1 = drawTextBlock(img_2, TEXT_HEIGHT, infos[1])
        pj.paste(img_2_1, (pic_width, pic_height, 2 * pic_width, pic_height + TEXT_HEIGHT))

        img_3 = infos[2][INFO[0]]
        pj.paste(img_3, (0, pic_height + TEXT_HEIGHT, pic_width, 2 * pic_height + TEXT_HEIGHT))
        img_3_1 = drawTextBlock(img_3, TEXT_HEIGHT, infos[2])
        pj.paste(img_3_1, (0, 2 * pic_height + TEXT_HEIGHT, pic_width,
                           2 * pic_height + 2 * TEXT_HEIGHT))

        img_4 = infos[3][INFO[0]]
        pj.paste(img_4, (pic_width, pic_height + TEXT_HEIGHT, 2 * pic_width, 2 * pic_height + TEXT_HEIGHT))
        img_4_1 = drawTextBlock(img_4, TEXT_HEIGHT, infos[3])
        pj.paste(img_4_1, (pic_width, 2 * pic_height + TEXT_HEIGHT, 2 * pic_width, 2 * pic_height + 2 * TEXT_HEIGHT))
        save_file_path = UPLOAD_FOLDER + "/" + form_data.get("fileName") + ".jpg"
        pj.save(save_file_path)

        closeImsge((img, img_1, img_1_1, img_2, img_2_1, img_3, img_3_1, img_4, img_4_1))
        with open(save_file_path, 'rb') as f:
            image = f.read()
            resp = Response(image, mimetype="image/jpg")
            return resp
        resp = Response(pj, mimetype="image/jpg")
        return resp
    return render_template('index.html')


def closeImsge(images: ()):
    for image in images:
        image.close()


def drawTextBlock(img, TEXT_HEIGHT, info):
    blank = Image.new("RGB", [img.size[0], TEXT_HEIGHT], "black")
    draw = ImageDraw.Draw(blank)
    font = ImageFont.truetype('simsun.ttc', 60)
    text = concatText(info)
    draw.text((0, 0), text, fill=(55, 251, 240), font=font)
    return blank


# # 查看图片
# @app.route("/photo/<imageId>.jpg")
# def get_frame(imageId):
#     # 图片上传保存的路径
#     with open(r'C:/dataAnalysis/pyWorkspace/pictureConcat/photo/{}.jpg'.format(imageId), 'rb') as f:
#         image = f.read()
#         resp = Response(image, mimetype="image/jpg")
#         return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
