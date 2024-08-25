from PIL import Image

def compress_image(input_path, output_path, max_width=40, max_height=40):
    with Image.open(input_path) as img:
        img.thumbnail((max_width, max_height))
        img.save(output_path, optimize=True, quality=85)

compress_image('web/static/img/gwc.jpg', 'web/static/img/gwc.jpg')
compress_image('web/static/img/lps.jpg', 'web/static/img/lps.jpg')
compress_image('web/static/img/stz.jpg', 'web/static/img/stz.jpg')
compress_image('web/static/img/wyh.jpg', 'web/static/img/wyh.jpg')
compress_image('web/static/img/zl.jpg', 'web/static/img/zl.jpg')
#记得删除 pillow库
