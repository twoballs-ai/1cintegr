import os
from flask import Flask, flash, render_template, url_for, request, \
    session, redirect, Blueprint
from flask import send_from_directory
from werkzeug.utils import secure_filename
import requests
from requests.structures import CaseInsensitiveDict
import json
import datetime
from dadata import Dadata
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

import auth
from auth import auth_func, validateAccesToken, refreshAccesToken, deleteTokens


datetime = datetime.datetime.now()
print(datetime)

UPLOAD_FOLDER = '/mnt/disk_d/upload'
UPLOAD_FOLDER_MULTI = '/mnt/disk_d/upload/multi'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
token = "d9d839eea6af5bf1c146189a65c734a35651b6f2"
secret = "6a40c77de8faddcc68c6f90d4de5cae8608767e3"





basedir = os.path.abspath(os.path.dirname(__file__))
# MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
#
# path = "/"
# print(path)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cdvfdjn43439acd9*&^$%&*&^%G&^%FGYH'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_MULTI'] = UPLOAD_FOLDER_MULTI

# аутентификация



blueprint = Blueprint('site', __name__, static_url_path='/static/site', static_folder='/mnt/disk_d/1c_media/')
app.register_blueprint(blueprint)
app.register_blueprint(auth_func)






# @app.route('/')
# @app.route('/index')
# def index():
#     print(url_for('index'))
#
#     return render_template('index.html')


# class MyForm(FlaskForm):
#     file = FileField('File')
#     submit = SubmitField('Submit')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/downloads', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#
# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/')
@app.route('/index')
@app.route('/podved')
@app.route('/podved/')
def podved(*args, **kwargs):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            print('valid')

            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # if key doesn't exist, returns None
            param_request = {'page': '1'}
            # response = requests.get(url, verify=False)
            response = requests.post(url, param_request, verify=False)
            # page = request.args.get('page', 1 ,type=int)
            # response = requests.get(url, verify=False)

            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_PD']
            context = {'data': data}
            print(data)
            return render_template('podved.html', **context)
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'podved'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))




@app.route('/category_podved/<id>')
@app.route('/category_podved/<id>/')
def category_podved(id):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            print('valid')
            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # if key doesn't exist, returns None
            param_request = {'page': '1',
                             'cat_code': id}
            # response = requests.get(url, verify=False)
            response = requests.post(url, param_request, verify=False)
            # page = request.args.get('page', 1 ,type=int)
            # response = requests.get(url, verify=False)

            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_PD']
            context = {'data': data}
            print(data)
            return render_template('podved.html', **context)
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'category_podved','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))


@app.route('/category')
@app.route('/category/')
def category():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            url = "https://localhost/copy_1/hs/HTTP_SERVER/category_objects_list"
            param_request = {'page': '1'}
            # print(param_request)
            response = requests.post(url, param_request, verify=False)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_cat']
            data1 = response.json()
            context = {'data': data}
            print(data)
            return render_template('category.html', **context)
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'category'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))


# @app.route('/category_objects/<id>')
# @app.route('/category_objects/<id>/')
# def categoryobjects(id):
#     url = "https://localhost/copy_1/hs/HTTP_SERVER/objects_list_by_cat"
#     # if key doesn't exist, returns None
#     param_request = {'code': id,
#                      'page': '1'}
#     # response = requests.get(url, verify=False)
#     response = requests.post(url, param_request, verify=False)
#     # page = request.args.get('page', 1 ,type=int)
#     # response = requests.get(url, verify=False)
#
#     if response.status_code == 200:
#         print('Success!')
#     elif response.status_code == 401:
#         print('Not auth.')
#     data = response.json()['list_OC']
#     context = {'data': data}
#     print(data)
#     return render_template('category_objects.html', **context)


# https://localhost/copy_1/hs/HTTP_SERVER/get_objects_list?code=
@app.route('/cardhouse/<id>', methods=['GET'])
@app.route('/cardhouse/<id>/', methods=['GET'])
def cardhouse(id):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_card"
            param_request = {'code': id}
            print(param_request)
            response = requests.post(url, param_request, verify=False)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()
            # print(data)
            context = {'data': data,
                       'id': id}
            print(context)
            return render_template('cardhouse.html', **context)
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'cardhouse','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))



@app.route('/cardhousedetail/<id>', methods=['GET', 'POST'])
@app.route('/cardhousedetail/<id>/', methods=['GET', 'POST'])
def cardhousedetail(id):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
            param_request = {'code': id}
            response = requests.get(url, param_request, verify=False)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()
            object_type_val = response.json()['DataTypes']['object_type']
            # print(object_type_val)
            context = {'data': data,
                       'object_type_val': object_type_val,
                       'id': id}
            # print(data)
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
                # print("response.text:\n{}\n\n".format(responsePost.text))
                return redirect(url_for('cardhousedetail', id=id))
            return render_template('cardhousedetail.html', **context)

    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'cardhousedetail','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
# @app.route('/addcardhousedetail', methods=['GET', 'POST'])
# @app.route('/addcardhousedetail/', methods=['GET', 'POST'])
# def addcardhousedetail():
#     if request.method == 'POST':
#         # inputState = request.form.get('inputState')
#         name = request.form.get('name')
#         # address_full = request.form.get('adress')
#         region = request.form.get('region')
#         area = request.form.get('area')
#         city = request.form.get('city')
#         settlement = request.form.get('settlement')
#         street = request.form.get('street')
#         house = request.form.get('house')
#         flat = request.form.get('flat')
#         postal_code = request.form.get('postal_code')
#         egrn_nomer = request.form.get('egrn')
#         kadastr = request.form.get('kadastr')
#         object_type = request.form.get('object')
#         object_area = request.form.get('object_area')
#         encumbrance = request.form.get('encumbr')
#         description = request.form.get('description')
#         post_request = {'region': region, 'area': area, 'city': city, 'settlement': settlement, 'street': street,
#                         'house': house, 'flat': flat, 'postal_code': postal_code, 'name': name,
#                         'egrn_nomer': egrn_nomer, 'kadastr': kadastr, 'object_type': object_type,
#                         'object_area': object_area, 'encumbrance': encumbrance, 'description': description, 'code': 'new_object'
#                         }
#         print(post_request)
#         responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
#                                      verify=False)
#         responsePost.encoding = "ANSI"
#         id = responsePost.json()['code']
#         # print(id)
#         print("response:\n{}\n\n".format(responsePost))
#         # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
#         # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
#         # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
#         # print("response.text:\n{}\n\n".format(response.text))  # Text Output
#         # print("response.json:\n{}\n\n".format(response.json()))
#         print("response.encoding:\n{}\n\n".format(responsePost.encoding))  # Узнать, какую кодировку использует Requests
#         print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
#         # print(responsePost.text)
#         # context = {'id': id}
#         # return render_template('cardhousedetail/id.html')
#         return redirect(url_for('cardhousedetail', id = id))
#     return render_template('addcardhousedetail.html')


# @app.route('/cardhousedetail/<id>/edit', methods=['GET', 'POST'])
# @app.route('/cardhousedetail/<id>/edit/', methods=['GET', 'POST'])
# def cardhousedetailEdit(id):
#     url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
#     param_request = {'code': id}
#     response = requests.get(url, param_request, verify=False)
#     if response.status_code == 200:
#         print('Success!')
#     elif response.status_code == 401:
#         print('Not auth.')
#     data = response.json()
#     context = {'data': data,
#                'id': id}
#     if request.method == 'POST':
#         address_full = request.form.get('adress')
#         egrn_nomer = request.form.get('egrn')
#         kadastr = request.form.get('kadastr')
#         object_type = request.form.get('object')
#         object_area = request.form.get('area')
#         encumbrance = request.form.get('encumbr')
#         post_request = {'address_full': address_full, 'egrn_nomer': egrn_nomer,
#                         'kadastr': kadastr, 'object_type': object_type,
#                         'object_area': object_area, 'encumbrance': encumbrance,
#                         'code': id
#                         }
#         responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
#                                      verify=False)
#         return redirect(url_for('cardhousedetail', id=id))
#     # print(context)
#     return render_template('trash/cardhousedetailedit.html', **context)

#
# @app.route('/cardhousedetail/<id>/editanother', methods=['GET', 'POST'])
# @app.route('/cardhousedetail/<id>/editanother/', methods=['GET', 'POST'])
# def cardhousedetailEditAnother(id):
#     url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
#     param_request = {'code': id}
#     # print(param_request)
#     response = requests.get(url, param_request, verify=False)
#     if response.status_code == 200:
#         print('Success!')
#     elif response.status_code == 401:
#         print('Not auth.')
#     data = response.json()
#     # print(data)
#     context = {'data': data,
#                'id': id}
#     if request.method == 'POST':
#         address_full = request.form.get('adress')
#         egrn_nomer = request.form.get('egrn')
#         kadastr = request.form.get('kadastr')
#         object_type = request.form.get('object')
#         object_area = request.form.get('area')
#         encumbrance = request.form.get('encumbr')
#         post_request = {'address_full': address_full, 'egrn_nomer': egrn_nomer,
#                         'kadastr': kadastr, 'object_type': object_type,
#                         'object_area': object_area, 'encumbrance': encumbrance,
#                         'code': id
#                         }
#         responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
#                                      verify=False)
#         return redirect(url_for('cardhousedetail', id=id))
#     # print(context)
#     return render_template('trash/cardhousedetaileditanother.html', **context)


# @app.route('/dadata')
# def dadata():
#     dadata = Dadata(token, secret)
#     response = dadata.clean("address", "мск сухонска 11/-89")
#     # print("response:\n{}\n\n".format(response))
#     # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
#     # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
#     # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
#     # print("response.text:\n{}\n\n".format(response.text))  # Text Output
#     # print("response.json:\n{}\n\n".format(response.json()))
#     # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
#     # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
#     # print(response.json())
#     # context = {'data': data}
#     # print(context)
#     print(response)
#
#     return response

# @app.route('/customers/<number>/', methods=['GET', 'POST'])
# def customers(number):
#     url = "https://localhost/copy_1/hs/HTTP_SERVER/objects_list"
#     number = int(number)
#
#     param_request = {'page': number}
#     number2 = param_request["page"]
#     response = requests.get(url, param_request, verify=False)
#     if response.status_code == 200:
#         print('Success!')
#     elif response.status_code == 401:
#         print('Not auth.')
#     data = response.json()['list_OC']
#     data1 = response.json()
#     context = {'data': data,
#                'number2': number2}
#     print(data, data1)
#     if request.method == 'POST':
#         # inputState = request.form.get('inputState')
#         name = request.form.get('name')
#         # address_full = request.form.get('adress')
#         region = request.form.get('region')
#         area = request.form.get('area')
#         city = request.form.get('city')
#         settlement = request.form.get('settlement')
#         street = request.form.get('street')
#         house = request.form.get('house')
#         flat = request.form.get('flat')
#         postal_code = request.form.get('postal_code')
#         egrn_nomer = request.form.get('egrn')
#         kadastr = request.form.get('kadastr')
#         object_type = request.form.get('object')
#         object_area = request.form.get('object_area')
#         encumbrance = request.form.get('encumbr')
#         description = request.form.get('description')
#         print('hello')
#         if 'file' not in request.files:
#             # После перенаправления на страницу загрузки
#             # покажем сообщение пользователю
#             flash('Не могу прочитать файл')
#             return redirect(request.url)
#         file = request.files['file']
#         # Если файл не выбран, то браузер может
#         # отправить пустой файл без имени.
#         if file.filename == '':
#             flash('Нет выбранного файла')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             # безопасно извлекаем оригинальное имя файла
#             filename = secure_filename(file.filename)
#             # сохраняем файл
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         foto_main = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)
#         # загрузка мультифото
#         if 'files[]' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         files = request.files.getlist('files[]')
#         foto_list = []
#         for file in files:
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER_MULTI'], filename))
#                 foto_list.append("%s/%s" % (app.config['UPLOAD_FOLDER_MULTI'], filename))
#         foto_multi = foto_list
#
#         post_request = {'region': region, 'area': area, 'city': city, 'settlement': settlement, 'street': street,
#                         'house': house, 'flat': flat, 'postal_code': postal_code, 'name': name,
#                         'egrn_nomer': egrn_nomer, 'kadastr': kadastr, 'object_type': object_type,
#                         'object_area': object_area, 'encumbrance': encumbrance, 'description': description,
#                         'foto_main': foto_main, 'foto_multi': foto_multi, 'code': 'new_object'
#                         }
#         print('fdbfdbf',post_request)
#         responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
#                                      verify=False)
#         responsePost.encoding = "ANSI"
#         id = responsePost.json()['code']
#         # print(id)
#         print("response:\n{}\n\n".format(responsePost))
#         print("response.encoding:\n{}\n\n".format(responsePost.encoding))  # Узнать, какую кодировку использует Requests
#         print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
#         # print(responsePost.text)
#         # context = {'id': id}
#         # return render_template('cardhousedetail/id.html')
#         return redirect(url_for('cardhousedetail', id=id))
#
#     return render_template('customers.html', **context)

@app.route('/customers/<id>/', methods=['GET', 'POST'])
def customers(id):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        print(valid)
        if valid == 'True':
            url = "https://localhost/copy_1/hs/HTTP_SERVER/objects_list"
            id = int(id)
            param_request = {'page': id}
            number2 = param_request["page"]
            response = requests.get(url, param_request, verify=False)

            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_OC']
            data1 = response.json()
            context = {'data': data,
                       'number2': number2}
            print(data)
            print(number2,param_request)

            if request.method == 'POST':
                # inputState = request.form.get('inputState')
                name = request.form.get('name')
                print(name)
                # address_full = request.form.get('adress')
                region = request.form.get('region')
                print(region)
                area = request.form.get('area')
                print(area)
                city = request.form.get('city')
                print(city)
                settlement = request.form.get('settlement')
                print(settlement)
                street = request.form.get('street')
                print(street)
                house = request.form.get('house')
                print(house)
                flat = request.form.get('flat')
                print(flat)
                postal_code = request.form.get('postal_code')
                print(postal_code)
                egrn_nomer = request.form.get('egrn')
                print(egrn_nomer)
                kadastr = request.form.get('kadastr')
                print(kadastr)
                object_type = request.form.get('object')
                object_area = request.form.get('object_area')
                print(object_area)
                encumbrance = request.form.get('encumbr')
                description = request.form.get('description')
                print(description, encumbrance, object_type )
                foto_main = ''
                print('dfdf',foto_main)
                if 'file' not in request.files:
                    # После перенаправления на страницу загрузки
                    # покажем сообщение пользователю
                    flash('Не могу прочитать файл')
                    print('проблема')
                    print('проблема',request.url)
                    return redirect(request.url)

                file = request.files['file']
                print(file)
                # Если файл не выбран, то браузер может
                # отправить пустой файл без имени.

                if file.filename == '':
                    foto_main = ''

                print('dfdf',foto_main)
                if file and allowed_file(file.filename):
                    # безопасно извлекаем оригинальное имя файла
                    filename = secure_filename(file.filename)
                    # сохраняем файл
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    foto_main = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)

                # # загрузка мультифото
                if 'files[]' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                files = request.files.getlist('files[]')
                foto_list = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER_MULTI'], filename))
                        foto_list.append("%s/%s" % (app.config['UPLOAD_FOLDER_MULTI'], filename))
                foto_multi = foto_list
                post_request = {'region': region, 'area': area, 'city': city, 'settlement': settlement, 'street': street,
                                'house': house, 'flat': flat, 'postal_code': postal_code, 'name': name,
                                'egrn_nomer': egrn_nomer, 'kadastr': kadastr, 'object_type': object_type,
                                'object_area': object_area, 'encumbrance': encumbrance, 'description': description,
                                'foto_main': foto_main, 'foto_multi': foto_multi, 'code': 'new_object'
                                }
                print(post_request)
                responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,
                                             verify=False)
                responsePost.encoding = "ANSI"
                id = responsePost.json()['code']
                # print(id)
                print("response:\n{}\n\n".format(responsePost))
                print("response.encoding:\n{}\n\n".format(responsePost.encoding))  # Узнать, какую кодировку использует Requests
                print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
                print("response.json:\n{}\n\n".format(response.json()))
                # print(responsePost.text)
                # context = {'id': id}
                # return render_template('cardhousedetail/id.html')
                return redirect(url_for('cardhousedetail', id=id))

            return render_template('customers.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'customers','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))

@app.route('/search')
@app.route('/search/')
def search():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            print(url_for('search'))
            return render_template('search.html', title='minkult-CRM')
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'search'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))



@app.route('/about')
@app.route('/about/')
def about():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            print(url_for('about'))
            return render_template('about.html', title='minkult-CRM')
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'about'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))



@app.route('/contacts')
@app.route('/contacts/')
def contacts():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            print(url_for('contacts'))
            return render_template('contacts.html', title='minkult-CRM')
        elif not valid:
            print('not_valid')
            return deleteTokens()
    elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        link_send_to_refresh = {'link':'contacts'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))



# @app.route('/profile/<username>')
# def profile(username):
#     return f'профиль пользователя {username}'


# пример создания ссылок
# @app.route('/url/<int:variable>/<variable>')


# роверка ссылок на правильность
# with app.test_request_context():
#     print(url_for('index'))

@app.errorhandler(404)
def pageNotFound(error):
    # if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
    #     valid = validateAccesToken()
    #     print('вас кинуло на 404')
    #     if valid:
    # print('valid')

    return render_template('page_404.html'), 404
        # elif not valid:
        #     print('not_valid')
        #     return deleteTokens()
    # elif not request.cookies.get('access_token') and request.cookies.get('refresh_token'):
    #     link_send_to_refresh = {'link':'pageNotFound'}
    #     refresh = refreshAccesToken(link_send_to_refresh)
    #     return refresh
    # elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
    #     return redirect(url_for('auth_func.login'))


if __name__ == '__main__':
    app.run(debug=True)
