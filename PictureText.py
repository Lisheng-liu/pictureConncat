from PIL import Image, ImageDraw, ImageFont

UPLOAD_FOLDER = "C:/Users/19508/Desktop/pictureConcatTest/20200309204514/"
img = Image.open(UPLOAD_FOLDER + "p1.jpg")
blank = Image.new("RGB", [img.size[0], 60], "black")
draw = ImageDraw.Draw(blank)
# draw.rectangle((0, 0, img.size[0], 30), fill=(255, 0, 0))
font = ImageFont.truetype('simsun.ttc', 30);
draw.text((0, 0), "中文测试\nCD", fill=(255,251,240), font=font)
pj = Image.new('RGB', (img.size[0]+200, img.size[1] + blank.size[1]+300))
pj.paste(img, (0, 0, img.size[0], img.size[1]))
pj.paste(blank, (0, img.size[1], img.size[0], img.size[1] + blank.size[1]))

pj.show()
blank.close()
img.close()
pj.close()


