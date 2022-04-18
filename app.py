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


@app.route('/search')
@app.route('/search/')
def search():
    print(url_for('search'))
    return render_template('search.html', title='minkult-CRM')


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


# @app.route('/query-example')
# def query_example():
#     # if key doesn't exist, returns None
#     param_request = {'key1': 'value1', 'key2': 'value2'}
#     response = requests.get("http://app.vafrike21.ru:8080/atma/hs/GradeReception/GetblankgradeBHS?GradeBlank=85ac3477-bbb6-11ec-8db8-049226b84f98", params=param_request)
#
#     print("response:\n{}\n\n".format(response))
#     print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
#     print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
#     print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
#     print("response.text:\n{}\n\n".format(response.text))  # Text Output
#     print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
#     print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
#     return "response.url:\n{}\n\n".format(response.url)

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
