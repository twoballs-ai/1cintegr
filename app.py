from flask import Flask, render_template, url_for, request, \
    session, redirect, Blueprint
import requests
import json

import os
# MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
#
# path = "/"
# print(path)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cdvfdjn43439acd9*&^$%&*&^%G&^%FGYH'

blueprint = Blueprint('site', __name__, static_url_path='/static/site', static_folder='/mnt/disk_d/1c_media/')
app.register_blueprint(blueprint)


@app.route('/')
@app.route('/index')
def index():
    print(url_for('index'))
    return render_template('index.html', title='minkult-CRM')


@app.route('/category')
@app.route('/category/')
def category():
    print(url_for('category'))
    return render_template('category.html', title='minkult-CRM')

# https://localhost/copy_1/hs/HTTP_SERVER/get_objects_list?code=
@app.route('/cardhouse/')
@app.route('/cardhouse/')
def cardhouse():
    print(url_for('cardhouse'))
    return render_template('cardhouse.html', title='minkult-CRM')


@app.route('/cardhousedetail/<id>', methods=['GET', 'POST'])
@app.route('/cardhousedetail/<id>/', methods=['GET', 'POST'])
def cardhousedetail(id):
    # print(id)
    url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
    param_request = {'code': id}
    # print(param_request)
    response = requests.get(url, param_request, verify=False)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()
    # print(data)
    context = {'data': data}
    datas = request.form
    print(datas)
    return render_template('cardhousedetail.html',  **context)



# @app.route('/customers/', methods=['POST'])
# @app.route('/customers/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text
#     print(processed_text)
#     return processed_text

@app.route('/customers')
@app.route('/customers/')
def customers():
    url = "https://localhost/copy_1/hs/HTTP_SERVER/objects_list"
    # if key doesn't exist, returns None
    param_request = {'page': '1', 'limitpage': '20'}
    # response = requests.get(url, verify=False)
    response = requests.get(url, param_request, verify=False)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()['list_OC']



    # print("json")
    # for i in img:
    #     if not i['dikpic']:
    #         print('gbcmrf')
    #         continue
    #     print(i['dikpic']['fotoAdr'])
        # img_response = i['dikpic']
    #     imgresponse = requests.get(img_response, param_request, verify=False)
    #
    #     print(imgresponse.text)
    # img_response = img[0]['dikpic']['fotoAdr']
    # print(img_response )
    # print("response:\n{}\n\n".format(response))
    # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    # print("response.text:\n{}\n\n".format(response.text))  # Text Output
    # print("response.json:\n{}\n\n".format(response.json()))
    # print("response.json:\n{}\n\n".format(data))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    # pprint((data)['list_OC'])
    context = {'data': data}
    return render_template('customers.html', **context)


@app.route('/search')
@app.route('/search/')
def search():
    print(url_for('search'))
    return render_template('search.html', title='minkult-CRM')


@app.route('/about')
@app.route('/about/')
def about():
    print(url_for('about'))
    return render_template('about.html', title='minkult-CRM')


@app.route('/contacts')
@app.route('/contacts/')
def contacts():
    print(url_for('contacts'))
    return render_template('contacts.html', title='minkult-CRM')


@app.route('/profile/<username>')
def profile(username):
    return f'профиль пользователя {username}'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST':
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация')


@app.route('/login2', methods=['POST', 'GET'])
def login2():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST':
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login2.html', title='Авторизация')


@app.route('/get')
def get():

    url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
    # if key doesn't exist, returns None
    param_request = {'code': '000000748'}
    # response = requests.get(url, verify=False)
    response = requests.get(url,param_request, verify=False )
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data= response.json()
    # print("response:\n{}\n\n".format(response))
    # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    # print("response.text:\n{}\n\n".format(response.text))  # Text Output
    # print("response.json:\n{}\n\n".format(response.json()))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    # print(response.json())
    context = {'data': data}
    return render_template('get.html', **context)

@app.route('/post')
def post(*args, **kwargs):
    # if key doesn't exist, returns None
    param_request = {'USR': 'test', 'PWD': '2200'}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/auth_chek", data=param_request, verify=False)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    print("response:\n{}\n\n".format(response))
    print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    print("response.text:\n{}\n\n".format(response.text))  # Text Output
    # print("response.json:\n{}\n\n".format(response.json()))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    return "response.text:\n{}\n\n".format(response.text)


# пример создания ссылок
# @app.route('/url/<int:variable>/<variable>')


# роверка ссылок на правильность
# with app.test_request_context():
#     print(url_for('index'))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page_404.html', title='страница не найдена'), 404


if __name__ == '__main__':
    app.run(debug=True)
