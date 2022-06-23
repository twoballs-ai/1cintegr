from flask import Flask, render_template, url_for, request, \
    session, redirect, Blueprint
import requests
import json
from dadata import Dadata

token = "d9d839eea6af5bf1c146189a65c734a35651b6f2"
secret = "6a40c77de8faddcc68c6f90d4de5cae8608767e3"
import os
# MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
#
# path = "/"
# print(path)
import requests
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cdvfdjn43439acd9*&^$%&*&^%G&^%FGYH'

blueprint = Blueprint('site', __name__, static_url_path='/static/site', static_folder='/mnt/disk_d/1c_media/')
app.register_blueprint(blueprint)


@app.route('/')
@app.route('/index')
def index():
    print(url_for('index'))

    return render_template('index.html')


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


@app.route('/cardhousedetail/<id>', methods=['GET'])
@app.route('/cardhousedetail/<id>/', methods=['GET'])
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
    context = {'data': data,
               'id': id}
    print(context)
    return render_template('cardhousedetail.html', **context)


@app.route('/addcardhousedetail', methods=['GET', 'POST'])
@app.route('/addcardhousedetail/', methods=['GET', 'POST'])
def addcardhousedetail():
    if request.method == 'POST':
        # inputState = request.form.get('inputState')
        name = request.form.get('name')
        # address_full = request.form.get('adress')
        region = request.form.get('region')
        area = request.form.get('area')
        city = request.form.get('city')
        settlement = request.form.get('settlement')
        street = request.form.get('street')
        house = request.form.get('house')
        flat = request.form.get('flat')
        postal_code = request.form.get('postal_code')
        egrn_nomer = request.form.get('egrn')
        kadastr = request.form.get('kadastr')
        object_type = request.form.get('object')
        object_area = request.form.get('object_area')
        encumbrance = request.form.get('encumbr')
        description = request.form.get('description')
        post_request = {'region': region, 'area': area, 'city': city, 'settlement': settlement, 'street': street,
                        'house': house, 'flat': flat, 'postal_code': postal_code, 'name': name,
                        'egrn_nomer': egrn_nomer, 'kadastr': kadastr, 'object_type': object_type,
                        'object_area': object_area, 'encumbrance': encumbrance, 'description': description, 'code': 'new_object'
                        }
        print(post_request)
        responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
                                     verify=False)
        id = responsePost.json()['code']
        print(id)
        # print(responsePost.text)
        # context = {'id': id}
        # return render_template('cardhousedetail/id.html')
        return redirect(url_for('cardhousedetail', id = id))
    return render_template('addcardhousedetail.html')


@app.route('/cardhousedetail/<id>/edit', methods=['GET', 'POST'])
@app.route('/cardhousedetail/<id>/edit/', methods=['GET', 'POST'])
def cardhousedetailEdit(id):
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
    context = {'data': data,
               'id': id}
    if request.method == 'POST':
        address_full = request.form.get('adress')
        egrn_nomer = request.form.get('egrn')
        kadastr = request.form.get('kadastr')
        object_type = request.form.get('object')
        object_area = request.form.get('area')
        encumbrance = request.form.get('encumbr')
        post_request = {'address_full': address_full, 'egrn_nomer': egrn_nomer,
                        'kadastr': kadastr, 'object_type': object_type,
                        'object_area': object_area, 'encumbrance': encumbrance,
                        'code': id
                        }
        responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
                                     verify=False)
        return redirect(url_for('cardhousedetail', id=id))
        # print("response:\n{}\n\n".format(responsePost))
        # print("response.url:\n{}\n\n".format(responsePost.url))  # Посмотреть формат URL (с параметрами)
        # print("response.headers:\n{}\n\n".format(responsePost.headers))  # Header of the request
        # print("response.status_code:\n{}\n\n".format(responsePost.status_code))  # Получить код ответа
        # print("response.text:\n{}\n\n".format(responsePost.text))  # Text Output
        # print("response.encoding:\n{}\n\n".format(responsePost.encoding))  # Узнать, какую кодировку использует Requests
        # print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
    # print(context)
    return render_template('cardhousedetailedit.html', **context)


@app.route('/dadata')
def dadata():
    dadata = Dadata(token, secret)
    response = dadata.clean("address", "мск сухонска 11/-89")
    # print("response:\n{}\n\n".format(response))
    # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    # print("response.text:\n{}\n\n".format(response.text))  # Text Output
    # print("response.json:\n{}\n\n".format(response.json()))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    # print(response.json())
    # context = {'data': data}
    # print(context)
    print(response)

    return response


@app.route('/customers/<number>/')
def customers(number):
    url = "https://localhost/copy_1/hs/HTTP_SERVER/objects_list"
    number = int(number)

    param_request = {'page': number}
    number2 = param_request["page"]
    print(number2)
    print(number)
    response = requests.get(url, param_request, verify=False)
    # page = request.args.get('page', 1 ,type=int)
    # response = requests.get(url, verify=False)

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

    # pprint((data)['list_OC'])
    # c=[]
    # for i in range(1,100):
    #     c.append(i)
    context = {'data': data,
               'number2': number2}

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
    print(context)
    return render_template('get.html', **context)


@app.route('/post')
def post(*args, **kwargs):
    # if key doesn't exist, returns None
    param_request = {"query": "москва хабар"}
    response = requests.post("https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address", data=param_request,
                             verify=False)
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
