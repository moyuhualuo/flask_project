import os
from app import app, db, Md_test  # 确保导入 db 和 Md_test


# import markdown2  # 不再需要导入 markdown2

def insert_txt(txt_file, author):
    with app.app_context():
        if os.path.exists(txt_file):
            with open(txt_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # 创建新的数据库条目
                new_entry = Md_test(
                    page='life',
                    author=author,
                    content=content,  # 存储纯文本内容
                    is_published=True,
                )

            # 添加到数据库并提交
                db.session.add(new_entry)
                db.session.commit()
                print(f"Text content from {txt_file} has been inserted into the database.")
        else:
            print(f"File {txt_file} does not exist.")
if __name__ == '__main__':

    insert_txt('web/static/text/demo.txt', 'life_test')