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

    insert_txt('static/text/demo.txt', '自学优缺分析')
    insert_txt('static/text/demo.txt', '合理利用身份资源')
    insert_txt('static/text/demo.txt', '体验信息时代')
    insert_txt('static/text/demo.txt', '图书馆宝藏')
    insert_txt('static/text/demo.txt', '重要的必要技能')
    insert_txt('static/text/demo.txt', '关于考证')
    insert_txt('static/text/demo.txt', '焦虑')
    insert_txt('static/text/demo.txt', '规划建议')
    insert_txt('static/text/demo.txt', '请善用Tools')
    insert_txt('static/text/demo.txt', '结尾的话')