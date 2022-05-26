from flask import Flask, render_template, url_for, request, \
    session, redirect
import requests
import json

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cdvfdjn43439acd9*&^$%&*&^%G&^%FGYH'


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


@app.route('/cardhousedetail')
@app.route('/cardhousedetail/')
def cardhousedetail():
    print(url_for('cardhousedetail'))
    return render_template('cardhousedetail.html', title='minkult-CRM')


@app.route('/customers')
@app.route('/customers/')
def customers():
    data = getcustomers()
    context = {'data': data}

    return render_template('customers.html', **context)


def getcustomers():
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
    print("response.json:\n{}\n\n".format(data))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    # pprint((data)['list_OC'])
    # print((data))

    return (data)


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
    datatop = getdata()
    context = {'datatop':datatop}


    return render_template('get.html', **context)


def getdata():
    url="https://localhost/copy_1/hs/HTTP_SERVER/get_objects_list?code=000000787"
    # if key doesn't exist, returns None
    # param_request = {'USR': 'test', 'PWD': '2200'}
    response = requests.get(url, verify=False)
    # response = requests.get(url, verify=False, param_request)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data= response.json()
    # print("response:\n{}\n\n".format(response))
    # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    print("response.text:\n{}\n\n".format(response.text))  # Text Output
    # print("response.json:\n{}\n\n".format(response.json()))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    # pprint((data)['list_OC'])
    return (data)

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
