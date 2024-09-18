import os


def rename_images(folder_path, new_name_format="{}.jpg"):
    # 获取文件夹中所有的文件
    files = os.listdir(folder_path)

    # 过滤出图片文件
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # 对图片文件进行重命名
    for index, filename in enumerate(image_files, start=1):
        old_path = os.path.join(folder_path, filename)
        new_filename = new_name_format.format(index)
        new_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")


# 文件夹路径
folder_path = r"E:\图片"  # 替换为你的图片文件夹路径

rename_images(folder_path)
