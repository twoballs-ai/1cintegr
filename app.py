import os
from flask import Flask, flash, render_template, url_for, request, \
    session, redirect, Blueprint, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
import json
import urllib.request
import requests
import datetime
from dadata import Dadata
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

import auth
from forms import ObjectListForm
from requests_obj import request_func, listDepartsments, post, get, getUserName
from auth import auth_func, validateAccesToken, refreshAccesToken, deleteTokens, getAccessToken
from wtforms import Form, BooleanField, StringField, validators

datetime = datetime.datetime.now()


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
app.register_blueprint(request_func)






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


def data_params_request():
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url_params = "https://localhost/copy_1/hs/HTTP_SERVER/RulesNewObjects"
    response_params = requests.get(url_params, verify=False, headers=headers)

    if response_params.status_code == 200:
        print('Success!')
    elif response_params.status_code == 401:
        print('Not auth.')
    data_params = response_params.json()
    # print(f"большой список значений {data_params}")
    return data_params



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

@app.route('/region')
@app.route('/region/')
def region():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            # print('valid')
            # url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # # if key doesn't exist, returns None
            # param_request = {'page': '1',
            #                  'cat_code': id}
            # # response = requests.get(url, verify=False)
            # response = requests.post(url, param_request, verify=False)
            # # page = request.args.get('page', 1 ,type=int)
            # # response = requests.get(url, verify=False)
            #
            # if response.status_code == 200:
            #     print('Success!')
            # elif response.status_code == 401:
            #     print('Not auth.')
            # data = response.json()['list_PD']
            # context = {'data': data}
            # print(data)
            # jsonPars()
            return render_template('future_template.html')
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'category_podved','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()


@app.route('/')
@app.route('/index')
@app.route('/podved')
@app.route('/podved/')
def podved(*args, **kwargs):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        data_params_request()
        if valid == 'True':
            headers_get = getAccessToken()
            headers = {'AccessToken':headers_get}
            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # if key doesn't exist, returns None
            breadcrumbs = "Подведомственные организации"
            param_request = {'page': '1'}
            # response = requests.get(url, verify=False)
            response = requests.post(url, param_request, verify=False, headers=headers)
            # page = request.args.get('page', 1 ,type=int)
            # response = requests.get(url, verify=False)

            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_PD']
            print(response.json())
            departments = listDepartsments()
            # print(departments)
            getusername = getUserName()
            context = {'data': data, 'departments': departments, 'getusername':getusername, 'breadcrumbs':breadcrumbs}
            print(response.headers)
            # функция вызова подведов и создания страницы для пользователей.
            c= auth.getPodved()
            podved = c[0]
            permission_see = c[1]
            # print(type(podved), type(permission_see))
            if permission_see == True:
                return render_template('podved.html', **context)
            else:
                return redirect(url_for('cardhouse',id = podved))
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'podved'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()

@app.route('/department/<id>')
@app.route('/department/<id>/')
def department(id):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            print('valid')
            headers_get = getAccessToken()
            headers = {'AccessToken':headers_get}
            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # if key doesn't exist, returns None
            param_request = {'page': '1', 'department':id}
            # response = requests.get(url, verify=False)
            response = requests.post(url, param_request, verify=False, headers=headers)
            # page = request.args.get('page', 1 ,type=int)
            # response = requests.get(url, verify=False)

            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_PD']
            departments = listDepartsments()
            getusername = getUserName()
            departid = id
            name_depart = request.args.get('value')
            breadcrumbs = "Категория подведомственной организации"
            context = {'data': data,
                       'departments': departments,
                       'getusername':getusername,
                       'name_depart':name_depart,
                       'departid':departid}
            # print(response.headers)
            print(context)
            # print(context)
            return render_template('podved.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link': 'podved'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()


@app.route('/category_podved/<id>', methods=['GET', 'POST'])
@app.route('/category_podved/<id>/', methods=['GET', 'POST'])
def category_podved(id, *args, **kwargs):
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            print('valid')
            headers_get = getAccessToken()
            headers = {'AccessToken':headers_get}
            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # if key doesn't exist, returns None
            param_request = {'page': '1',
                             'cat_code': id}
            # response = requests.get(url, verify=False)
            response = requests.post(url, param_request, verify=False, headers=headers)
            # page = request.args.get('page', 1 ,type=int)
            # response = requests.get(url, verify=False)

            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_PD']
            departments = listDepartsments()
            getusername = getUserName()
            id_podved = id
            name_category_breadcrumbs = request.args.get('name')

            breadcrumbs = "Категория подведомственной организации"
            context = {'data': data,
                       'departments': departments,
                       'getusername':getusername,
                       'namebreadcrumbsbycat':name_category_breadcrumbs,
                       'breadcrumbs': breadcrumbs,
                       'id_podved':id_podved
                       }
            print(context)
            return render_template('podved.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'category_podved','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()


@app.route('/category')
@app.route('/category/')
def category():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            url = "https://localhost/copy_1/hs/HTTP_SERVER/category_objects_list"
            param_request = {'page': '1'}
            # print(param_request)
            headers_get = getAccessToken()
            headers = {'AccessToken':headers_get}
            response = requests.post(url, param_request, verify=False, headers=headers)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_cat']
            data1 = response.json()
            print(data1)
            departments = listDepartsments()
            getusername = getUserName()
            breadcrumbs = "Категория подведомственной организации"
            context = {'data': data, 'departments': departments, 'getusername':getusername, 'breadcrumbs': breadcrumbs}
            print(data)
            return render_template('category.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'category'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()


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
        if valid == 'True':
            url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_card"
            param_request = {'code': id}
            print(param_request)
            headers_get = getAccessToken()
            headers = {'AccessToken':headers_get}
            response = requests.post(url, param_request, verify=False, headers=headers)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()
            print(data)
            departments = listDepartsments()
            getusername = getUserName()
            id_podved = request.args.get('id_podv')
            id_podved_name = request.args.get('namebreadcrumbsbycat')
            departId = request.args.get('departments')
            departName = request.args.get('departmentsname')
            context = {'data': data,
                       'id': id,
                       'departments': departments,
                       'getusername': getusername,
                       'id_podved': id_podved,
                       'id_podved_name': id_podved_name,
                       'departId':departId,
                       'departName':departName
                       }
            print(departName)
            return render_template('cardhouse.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'cardhouse','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()


@app.route('/cardhousedetail/<id>', methods=['GET', 'POST'])
@app.route('/cardhousedetail/<id>/', methods=['GET', 'POST'])
def cardhousedetail(id):
    # global foto_scan
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            headers_get = getAccessToken()
            headers = {'AccessToken': headers_get}
            url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
            param_request = {'code': id}
            response = requests.get(url, param_request, verify=False,headers=headers)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()
            print(data)
            object_type_val = response.json()['object_type']
            data_params = data_params_request()
            # print(data_params)
            # print(object_type_val)
            departments = listDepartsments()
            getusername = getUserName()
            idpodv = request.args.get('idpodv')
            namepodv = request.args.get('namepodved')
            idcat_podved = request.args.get('idcat_podved')
            idcat_podvedname = request.args.get('idcat_podvedname')
            namepodved = request.args.get('namepodved')
            breadcrumbs_customers = "Объекты недвижимости"
            departId = request.args.get('departId')
            departname = request.args.get('departname')
            iddepartpodved = request.args.get('iddepartpodved')
            namedepartpodved =request.args.get('namedepartpodved')
            context = {'data': data,
                       'object_type_val': object_type_val,
                       'id': id,
                       'data_params': data_params,
                       'departments': departments,
                       'getusername':getusername,
                       'breadcrumbs_customers':breadcrumbs_customers,
                       'idpodv':idpodv,
                       'namepodv':namepodv,
                       'idcat_podved':idcat_podved,
                       'idcat_podvedname':idcat_podvedname,
                       'namepodved':namepodved,
                       'departId':departId,
                       'departname':departname,
                       'iddepartpodved':iddepartpodved,
                       'namedepartpodved':namedepartpodved}
            print(iddepartpodved)
            if request.method == 'POST':
                # 1шаг
                name = request.form.get('name')
                description = request.form.get('description')
                object_type = request.form.get('object_type')
                PurposeObject = request.form.get('PurposeObject')
                Condition = request.form.get('Condition')
                technicalFloor = request.form.get('technicalFloor')
                Lift = request.form.get('Lift')
                remontDate = request.form.get('remontDate')
                SecurityObligation = request.form.get('SecurityObligation')
                # if 'file' not in request.files:
                #     # После перенаправления на страницу загрузки
                #     # покажем сообщение пользователю
                #     flash('Не могу прочитать файл')
                #     print('проблема')
                #     print('проблема', request.url)
                #     return redirect(request.url)
                #
                # file = request.files['file']
                # print(file)
                # # Если файл не выбран, то браузер может
                # # отправить пустой файл без имени.
                #
                # if file.filename == '':
                #     foto_scan = ''
                #
                #     print('dfdf', foto_scan)
                # if file and allowed_file(file.filename):
                #     # безопасно извлекаем оригинальное имя файла
                #     filename = secure_filename(file.filename)
                #     # сохраняем файл
                #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #     foto_scan = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)
                region = request.form.get('region')
                address = request.form.get('address')
                object_area = request.form.get('object_area')
                LandCategory = request.form.get('LandCategory')
                TypeOfPermittedUse = request.form.get('TypeOfPermittedUse')
                print('название:', name)
                print('description:', description)
                print('object_type:', object_type)
                print('PurposeObject:', PurposeObject)
                print('region:', region)
                print('address:', address)
                print('object_area:', object_area)
                print('LandCategory:', LandCategory)
                print('TypeOfPermittedUse:', TypeOfPermittedUse)
                # 2 шаг
                print('2шаг')
                RNFI = request.form.get('RNFI')
                RNFI_date = request.form.get('RNFI_date')
                owner_nomer = request.form.get('owner_nomer')
                owner_date = request.form.get('owner_date')
                RecordNumberVEGRP = request.form.get('RecordNumberVEGRP')
                DateRecordsVEGRP = request.form.get('DateRecordsVEGRP')
                TypeofRightOwner = request.form.get('TypeofRightOwner')
                BalanceAccountNumber = request.form.get('BalanceAccountNumber')
                date_of_registration_of_another_right = request.form.get('date_of_registration_of_another_right')
                inventory_number = request.form.get('inventory_number')
                balance_number = request.form.get('balance_number')
                CadastralNumber = request.form.get('CadastralNumber')
                Date_of_assignment_cadastral = request.form.get('Date_of_assignment_cadastral')
                cadastralcost = request.form.get('cadastralcost')
                Initial_cost = request.form.get('Initial_cost')
                residual_value = request.form.get('residual_value')
                print('RNFI:', RNFI)
                print('RNFI_date:', RNFI_date)
                print('owner_nomer:', owner_nomer)
                print('owner_date:', owner_date)
                print('RecordNumberVEGRP:', RecordNumberVEGRP)
                print('DateRecordsVEGRP:', DateRecordsVEGRP)
                print('TypeofRightOwner:', TypeofRightOwner)
                print('BalanceAccountNumber:', BalanceAccountNumber)
                print('date_of_registration_of_another_right:', date_of_registration_of_another_right)
                print('inventory_number:', inventory_number)
                print('balance_number:', balance_number)
                print('CadastralNumber:', CadastralNumber)
                print('Date_of_assignment_cadastral:', Date_of_assignment_cadastral)
                print('cadastralcost:', cadastralcost)
                print('Initial_cost:', Initial_cost)
                print('residual_value:', residual_value)
                # 3 шаг
                print('3шаг')
                historical_Category = request.form.get('historical_Category')
                UGROKN_number = request.form.get('UGROKN_number')
                print('historical_Category:', historical_Category)
                print('UGROKN_number:', UGROKN_number)
                # 4 шаг
                print('4шаг')
                KindEncumbrances = request.form.get('KindEncumbrances')
                encumbrance_area = request.form.get('encumbrance_area')
                encumbrance_cost = request.form.get('encumbrance_cost')
                person_encumbrance = request.form.get('person_encumbrance')
                Other_payments = request.form.get('Other_payments')
                start_encumbrance = request.form.get('start_encumbrance')
                end_encumbrance = request.form.get('end_encumbrance')
                start_use = request.form.get('start_use')
                end_use = request.form.get('end_use')
                Payment_foruse = request.form.get('Payment_foruse')
                print('KindEncumbrances:', KindEncumbrances)
                print('encumbrance_area:', encumbrance_area)
                print('encumbrance_cost:', encumbrance_cost)
                print('person_encumbrance:', person_encumbrance)
                print('Other_payments:', Other_payments)
                print('start_encumbrance:', start_encumbrance)
                print('end_encumbrance:', end_encumbrance)
                print('start_use:', start_use)
                print('end_use:', end_use)
                print('Payment_foruse:', Payment_foruse)

                # if 'file' not in request.files:
                #     # После перенаправления на страницу загрузки
                #     # покажем сообщение пользователю
                #     flash('Не могу прочитать файл')
                #     print('проблема')
                #     print('проблема', request.url)
                #     return redirect(request.url)
                #
                # file = request.files['file']
                # print(file)
                # # Если файл не выбран, то браузер может
                # # отправить пустой файл без имени.
                #
                # if file.filename == '':
                #     foto_main = ''
                #
                #     print('dfdf', foto_main)
                # if file and allowed_file(file.filename):
                #     # безопасно извлекаем оригинальное имя файла
                #     filename = secure_filename(file.filename)
                #     # сохраняем файл
                #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #     foto_main = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)
                #
                # # # загрузка мультифото
                # if 'files[]' not in request.files:
                #     flash('No file part')
                #     return redirect(request.url)
                # files = request.files.getlist('files[]')
                # foto_list = []
                # for file in files:
                #     if file and allowed_file(file.filename):
                #         filename = secure_filename(file.filename)
                #         file.save(os.path.join(app.config['UPLOAD_FOLDER_MULTI'], filename))
                #         foto_list.append("%s/%s" % (app.config['UPLOAD_FOLDER_MULTI'], filename))
                # foto_multi = foto_list
                # print('foto_main',foto_main)
                # print('foto_multi',foto_multi)
                post_request = {'name': name, 'description': description, 'object_type': object_type,
                                'PurposeObject': PurposeObject,'Condition':Condition,'technicalFloor':technicalFloor,
                                'Lift': Lift,'remontDate': remontDate,'SecurityObligation': SecurityObligation,
                                'region':region,'address':address,
                                # 'foto_scan':foto_scan,
                                'object_area': object_area, 'LandCategory': LandCategory,
                                'TypeOfPermittedUse': TypeOfPermittedUse,
                                'RNFI': RNFI, 'RNFI_date': RNFI_date, 'owner_nomer': owner_nomer,
                                'owner_date': owner_date,
                                'RecordNumberVEGRP': RecordNumberVEGRP, 'DateRecordsVEGRP': DateRecordsVEGRP,
                                'TypeofRightOwner': TypeofRightOwner, 'BalanceAccountNumber': BalanceAccountNumber,
                                'date_of_registration_of_another_right': date_of_registration_of_another_right,
                                'inventory_number': inventory_number, 'balance_number': balance_number,
                                'CadastralNumber': CadastralNumber,
                                'Date_of_assignment_cadastral': Date_of_assignment_cadastral,
                                'cadastralcost': cadastralcost, 'Initial_cost': Initial_cost,
                                'residual_value': residual_value,
                                'historical_Category': historical_Category, 'UGROKN_number': UGROKN_number,
                                'KindEncumbrances': KindEncumbrances,
                                'encumbrance_area': encumbrance_area, 'encumbrance_cost': encumbrance_cost,
                                'person_encumbrance': person_encumbrance, 'Other_payments': Other_payments,
                                'start_encumbrance': start_encumbrance, 'end_encumbrance': end_encumbrance,
                                'start_use': start_use, 'end_use': end_use, 'Payment_foruse': Payment_foruse,
                                'code': id
                                }
                print(post_request)
                responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,headers=headers,
                                             verify=False)
                # print("response.json:\n{}\n\n".format(responsePost.json()))
                print("response.text:\n{}\n\n".format(responsePost.text))
                return redirect(url_for('cardhousedetail', id=id))
            return render_template('cardhousedetail.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'cardhousedetail','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()
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
@app.route('/customers/<id>', methods=['GET', 'POST'])
def customers(id):


    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        print(valid)
        if valid == 'True':

            headers_get = getAccessToken()
            headers = {'AccessToken':headers_get}
            url = ("https://localhost/copy_1/hs/HTTP_SERVER/objects_list")
            id = int(id)
            filter = request.args.get('filter')
            sort = request.args.get('sort')
            param_request = {'page': id, 'filter': filter, 'sort': sort}
            number2 = param_request["page"]
            response = requests.get(url, param_request, verify=False, headers=headers)
            print(filter)
            if response.status_code == 200:
                print('Success!')
            elif response.status_code == 401:
                print('Not auth.')
            data = response.json()['list_OC']
            data1 = response.json()
            print(param_request)
            form = ObjectListForm()
            print(number2,param_request)
            # парсинг валидации и тех даных
            data_params = data_params_request()
            departments = listDepartsments()
            getusername = getUserName()
            breadcrumbs = "Объекты недвижимости"
            context = {'data': data, 'data_params': data_params,
                       'number2': number2,
                       'departments': departments,
                       'getusername':getusername,
                       'breadcrumbs': breadcrumbs,
                       'filter':filter}
            # print(context)
            if request.method == 'POST':
            # if form.validate_on_submit():


                            # 1шаг
                name = request.form.get('name')
                # name = form.name.data
                description = request.form.get('description')
                object_type = request.form.get('object_type')
                PurposeObject = request.form.get('PurposeObject')
                Condition = request.form.get('Condition')
                technicalFloor = request.form.get('technicalFloor')
                Lift = request.form.get('Lift')
                remontDate = request.form.get('remontDate')
                SecurityObligation = request.form.get('SecurityObligation')
                # if 'file' not in request.files:
                #     # После перенаправления на страницу загрузки
                #     # покажем сообщение пользователю
                #     flash('Не могу прочитать файл')
                #     print('проблема')
                #     print('проблема', request.url)
                #     return redirect(request.url)
                #
                # file = request.files['file']
                # print(file)
                # # Если файл не выбран, то браузер может
                # # отправить пустой файл без имени.
                #
                # if file.filename == '':
                #     foto_scan = ''
                #
                #     print('dfdf', foto_scan)
                # if file and allowed_file(file.filename):
                #     # безопасно извлекаем оригинальное имя файла
                #     filename = secure_filename(file.filename)
                #     # сохраняем файл
                #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #     foto_scan = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)
                region = request.form.get('region')
                address = request.form.get('address')
                object_area = request.form.get('object_area')
                LandCategory = request.form.get('LandCategory')
                TypeOfPermittedUse = request.form.get('TypeOfPermittedUse')
                print('название:', name)
                print('description:',description)
                print('object_type:',object_type)
                print('PurposeObject:',PurposeObject)
                print('Condition',Condition)
                print('technicalFloor',technicalFloor)
                print('Lift',Lift)
                print('remontDate',remontDate)
                print('SecurityObligation',SecurityObligation)
                print('region:',region)
                print('address:',address)
                print('remontDate:',remontDate)
                print('object_area:',object_area)
                print('LandCategory:',LandCategory)
                print('TypeOfPermittedUse:',TypeOfPermittedUse)
                # 2 шаг
                print('2шаг')
                RNFI = request.form.get('RNFI')
                RNFI_date = request.form.get('RNFI_date')
                owner_nomer = request.form.get('owner_nomer')
                owner_date = request.form.get('owner_date')
                RecordNumberVEGRP = request.form.get('RecordNumberVEGRP')
                DateRecordsVEGRP = request.form.get('DateRecordsVEGRP')
                TypeofRightOwner = request.form.get('TypeofRightOwner')
                BalanceAccountNumber = request.form.get('BalanceAccountNumber')
                date_of_registration_of_another_right = request.form.get('date_of_registration_of_another_right')
                inventory_number = request.form.get('inventory_number')
                balance_number = request.form.get('balance_number')
                CadastralNumber = request.form.get('CadastralNumber')
                Date_of_assignment_cadastral = request.form.get('Date_of_assignment_cadastral')
                cadastralcost = request.form.get('cadastralcost')
                Initial_cost = request.form.get('Initial_cost')
                residual_value = request.form.get('residual_value')
                print('RNFI:', RNFI)
                print('RNFI_date:', RNFI_date)
                print('owner_nomer:', owner_nomer)
                print('owner_date:', owner_date)
                print('RecordNumberVEGRP:', RecordNumberVEGRP)
                print('DateRecordsVEGRP:', DateRecordsVEGRP)
                print('TypeofRightOwner:', TypeofRightOwner)
                print('BalanceAccountNumber:', BalanceAccountNumber)
                print('date_of_registration_of_another_right:', date_of_registration_of_another_right)
                print('inventory_number:', inventory_number)
                print('balance_number:', balance_number)
                print('CadastralNumber:', CadastralNumber)
                print('Date_of_assignment_cadastral:', Date_of_assignment_cadastral)
                print('cadastralcost:', cadastralcost)
                print('Initial_cost:', Initial_cost)
                print('residual_value:', residual_value)
                 # 3 шаг
                print('3шаг')
                historical_Category = request.form.get('historical_Category')
                UGROKN_number = request.form.get('UGROKN_number')
                print('historical_Category:', historical_Category)
                print('UGROKN_number:', UGROKN_number)
                # 4 шаг
                print('4шаг')
                KindEncumbrances = request.form.get('KindEncumbrances')
                encumbrance_area = request.form.get('encumbrance_area')
                encumbrance_cost = request.form.get('encumbrance_cost')
                person_encumbrance = request.form.get('person_encumbrance')
                Other_payments = request.form.get('Other_payments')
                start_encumbrance = request.form.get('start_encumbrance')
                end_encumbrance = request.form.get('end_encumbrance')
                start_use = request.form.get('start_use')
                end_use = request.form.get('end_use')
                Payment_foruse = request.form.get('Payment_foruse')
                print('KindEncumbrances:', KindEncumbrances)
                print('encumbrance_area:', encumbrance_area)
                print('encumbrance_cost:', encumbrance_cost)
                print('person_encumbrance:', person_encumbrance)
                print('Other_payments:', Other_payments)
                print('start_encumbrance:', start_encumbrance)
                print('end_encumbrance:', end_encumbrance)
                print('start_use:', start_use)
                print('end_use:', end_use)
                print('Payment_foruse:', Payment_foruse)
                # if 'file' not in request.files:
                #     # После перенаправления на страницу загрузки
                #     # покажем сообщение пользователю
                #     flash('Не могу прочитать файл')
                #     print('проблема')
                #     print('проблема',request.url)
                #     return redirect(request.url)
                foto_main = request.files['formFile']
                print(foto_main)
                # Если файл не выбран, то браузер может
                # отправить пустой файл без имени.

                if foto_main.filename == '':
                    print('название фото не может быть пустым',foto_main)

                if foto_main and allowed_file(foto_main.filename):
                    # безопасно извлекаем оригинальное имя файла
                    filename = secure_filename(foto_main.filename)
                    print(filename)
                    # сохраняем файл
                    foto_main.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    foto_main = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)



                # # загрузка мультифото
                # if 'files[]' not in request.files:
                #     flash('No file part')
                #     return redirect(request.url)
                files = request.files.getlist('files[]')
                foto_list = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER_MULTI'], filename))
                        foto_list.append("%s/%s" % (app.config['UPLOAD_FOLDER_MULTI'], filename))
                foto_multi = foto_list
                post_request = {'name': name, 'description':description,'object_type':object_type,
                                'PurposeObject':PurposeObject,'Condition':Condition,'technicalFloor':technicalFloor,
                                'Lift': Lift,'remontDate': remontDate,'SecurityObligation': SecurityObligation,
                                'region':region,'address':address,
                                # 'foto_scan':foto_scan,
                                'object_area':object_area,'LandCategory':LandCategory,
                                'TypeOfPermittedUse':TypeOfPermittedUse,
                                'RNFI': RNFI,'RNFI_date': RNFI_date,'owner_nomer': owner_nomer,'owner_date': owner_date,
                                'RecordNumberVEGRP': RecordNumberVEGRP,'DateRecordsVEGRP': DateRecordsVEGRP,
                                'TypeofRightOwner': TypeofRightOwner,'BalanceAccountNumber': BalanceAccountNumber,
                                'date_of_registration_of_another_right': date_of_registration_of_another_right,
                                'inventory_number': inventory_number,'balance_number': balance_number,
                                'CadastralNumber': CadastralNumber,
                                'Date_of_assignment_cadastral': Date_of_assignment_cadastral,
                                'cadastralcost': cadastralcost,'Initial_cost': Initial_cost,
                                'residual_value': residual_value,
                                'historical_Category': historical_Category,'UGROKN_number': UGROKN_number,
                                'KindEncumbrances':KindEncumbrances,
                                'encumbrance_area': encumbrance_area,'encumbrance_cost': encumbrance_cost,
                                'person_encumbrance': person_encumbrance,'Other_payments': Other_payments,
                                'start_encumbrance': start_encumbrance,'end_encumbrance': end_encumbrance,
                                'start_use': start_use,'end_use':end_use,'Payment_foruse':Payment_foruse,
                                'foto_main': foto_main, 'foto_multi': foto_multi, 'code': 'new_object'
                                }
                print(post_request)
                responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=post_request,headers=headers,
                                             verify=False)
                # responsePost.encoding = "ANSI"
                id = responsePost.json()['code']
                print(id)
                print("response:\n{}\n\n".format(responsePost))
                print("response.encoding:\n{}\n\n".format(responsePost.encoding))  # Узнать, какую кодировку использует Requests
                print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
                print("response.json:\n{}\n\n".format(responsePost.json()))
                print(responsePost.text)
                # context = {'id': id}
                # return render_template('cardhousedetail/id.html')

                return redirect(url_for('cardhousedetail', id=id))

            return render_template('customers.html', **context, form=form)
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
    else:
        return deleteTokens()


@app.route('/search')
@app.route('/search/')
def search():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            # headers_get = getAccessToken()
            # headers = {'AccessToken':headers_get}
            print(url_for('search'))
            departments = listDepartsments()
            getusername = getUserName()
            breadcrumbs = "Поиск"
            context = {'departments': departments, 'getusername': getusername, 'breadcrumbs': breadcrumbs}
            return render_template('search.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'search'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()

@app.route('/reports')
@app.route('/reports/')
def reports():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
        #     headers_get = getAccessToken()
        #     headers = {'AccessToken':headers_get}
            # print('valid')
            # url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
            # # if key doesn't exist, returns None
            # param_request = {'page': '1',
            #                  'cat_code': id}
            # # response = requests.get(url, verify=False)
            # response = requests.post(url, param_request, verify=False)
            # # page = request.args.get('page', 1 ,type=int)
            # # response = requests.get(url, verify=False)
            #
            # if response.status_code == 200:
            #     print('Success!')
            # elif response.status_code == 401:
            #     print('Not auth.')
            # data = response.json()['list_PD']
            # context = {'data': data}
            # print(data)
            departments = listDepartsments()
            getusername = getUserName()
            breadcrumbs = "Отчеты"
            context = {'departments': departments, 'getusername': getusername, 'breadcrumbs': breadcrumbs }
            return render_template('reports.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'category_podved','id':id}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()

@app.route('/about')
@app.route('/about/')
def about():
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            print(url_for('about'))
            departments = listDepartsments()
            getusername = getUserName()
            breadcrumbs = "О проекте"
            context = {'departments': departments, 'getusername': getusername, 'breadcrumbs':breadcrumbs}
            return render_template('about.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
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
        if valid == 'True':
            print(url_for('contacts'))
            departments = listDepartsments()
            getusername = getUserName()
            breadcrumbs = "Контакты"
            context = {'departments': departments, 'getusername': getusername, 'breadcrumbs':breadcrumbs}
            return render_template('contacts.html', **context)
        else:
            return deleteTokens()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        link_send_to_refresh = {'link':'contacts'}
        refresh = refreshAccesToken(link_send_to_refresh)
        return refresh
    elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
        print('шляпа2')
        return deleteTokens()
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return redirect(url_for('auth_func.login'))
    else:
        return deleteTokens()



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
    # elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
    #     link_send_to_refresh = {'link':'pageNotFound'}
    #     refresh = refreshAccesToken(link_send_to_refresh)
    #     return refresh
    # elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
    #     return redirect(url_for('auth_func.login'))


if __name__ == '__main__':
    app.run(host='10.0.0.13')
    # app.run(debug=True)
