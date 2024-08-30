# insert_data.py
from app import app


def insert_data(id_type, url, name, description):
    with app.app_context():
        data_entry = Web(id_type=id_type, link_url=url, link_name=name, description=description)
        try:
            # 添加数据到数据库
            db.session.add(data_entry)
            db.session.commit()
            print('数据插入成功')
        except Exception as e:
            db.session.rollback()
            print(f'插入数据时发生错误: {e}')


if __name__ == '__main__':
    datas = []
    while True:
        print('app / web / book or q:')
        id = input()
        if id =='q':
            break
        print('url:')
        url = input()
        print('name:')
        name = input()
        print('description:')
        description = input()
        datas.append((id, url, name, description))
    for data in datas:
        insert_data(data[0], data[1], data[2], data[3])
