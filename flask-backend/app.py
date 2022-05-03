import pymysql
from flask import Flask, request
from flask_cors import CORS
import json
from face_rec import FaceRec, faces
from PIL import Image
import base64
import io
import os
import shutil
import time

app = Flask(__name__)
CORS(app)


def sql_test(name):
    result = []
    db = pymysql.connect(host='localhost', user='root', db='test', password='1234', charset='utf8')
    curs = db.cursor()
    sql = 'select * from tbl_test where name="' + name + '"'
    curs.execute(sql)
    rows = curs.fetchall()
    for e in rows:
        temp = {'id': e[0], 'name': e[1], 'pw': e[2]}
        result.append(temp)
    db.commit()
    db.close()
    return result


@app.route('/test', methods=['POST', 'GET'])
def test():
    data = request.get_json()
    result = data['data']
    print('react data: ', result)
    sql_result = sql_test(result)
    print('sql: ', sql_result)  # [{'id': 3, 'name': 'jung', 'pw': '3'}]
    return {'username': sql_result[0]['name'], 'password': sql_result[0]['pw']}


@app.route('/api', methods=['POST', 'GET'])
def api():
    data = request.get_json()
    resp = 'Not Found'
    directory = './stranger'
    if data:
        if os.path.exists(directory):
            shutil.rmtree(directory)

        if not os.path.exists(directory):
            try:
                os.mkdir(directory)
                time.sleep(1)
                result = data['data']
                b = bytes(result, 'utf-8')
                image = b[b.find(b'/9'):]
                im = Image.open(io.BytesIO(base64.b64decode(image)))
                im.save(directory + '/stranger.jpeg')  # save captured picture from react webcam

                find_face = faces.recognize_faces()
                print(find_face)
                if find_face:
                    resp = find_face
                else:
                    resp = 'Not Found'
            except:
                pass
    return resp


if __name__ == '__main__':
    app.run()
