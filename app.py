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


# 上传图片
@app.route("/photo/upload", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        # file = request.files['file']
        files = request.files
        FILE = ['file1', 'file2', 'file3', 'file4']
        succ = 0
        id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = UPLOAD_FOLDER + '/' + id
        os.mkdir(path)
        os.chmod(path, stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
        for f in FILE:
            file = files[f]
            if file and allowed_file(file.filename):
                print(file.filename)
                # secure_filename方法会去掉文件名中的中文
                # file_name = secure_filename(file.filename)
                file_name = file.filename

                # path = os.path.join(app.config['UPLOAD_FOLDER'])

                # 保存图片
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                file.save(path + '/' + file_name)
                succ += 1
        if succ == len(FILE):
            print('upload success')
            image_compose(path)
            with open(path + "//final.jpg", 'rb') as f:
                image = f.read()
                resp = Response(image, mimetype="image/jpg")
                return resp
        else:
            return "upload file fail"
    return render_template('index.html')



# 查看图片
@app.route("/photo/<imageId>.jpg")
def get_frame(imageId):
    # 图片上传保存的路径
    with open(r'C:/dataAnalysis/pyWorkspace/pictureConcat/photo/{}.jpg'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
