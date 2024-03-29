import os
import requests
import auth
from flask import render_template, url_for, request, \
    redirect, make_response
from flask.views import View, MethodView
from werkzeug.utils import secure_filename
from PIL import Image
import config
import os.path
from config import ALLOWED_EXTENSIONS
from transliterate import translit, get_available_language_codes
from models import podved_list, category_objects_list, podved_card, object_card, objects_list
from requests_obj import listDepartsments, getUserName, data_params_request
from auth import validateAccesToken, refreshAccesToken, deleteTokens, getAccessToken


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Index(View):
    def dispatch_request(self, id):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            data_params_request()
            if valid == 'True':
                breadcrumbs = "Подведомственные организации"
                id = int(id)
                filter = request.cookies.get('filter')
                param_request = {'page': id, 'filter':filter}
                page = param_request["page"]
                # берем данные из файла модели
                data = podved_list(param_request)['list_PD']
                page_info = podved_list(param_request)['Page_info']
                print(page_info)
                max_page = int(page_info['NumberOfPages'])
                pageNumber1C = int(page_info['PageNumber'])
                print(param_request)
                departments = listDepartsments()
                # print(departments)
                getusername = getUserName()
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'data': data, 'departments': departments, 'getusername': getusername,
                           'page': page,'filter':filter, 'max_page': max_page, 'pageNumber1C': pageNumber1C,
                           'breadcrumbs': breadcrumbs, 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}
                # функция вызова подведов и создания страницы для пользователей.
                print('отладка')
                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                if permission_see == True:
                    return render_template('podved.html', **context)
                else:
                    need_confirm_contacts = auth.updatePodvedInfo()
                    if need_confirm_contacts == True:
                        return redirect(url_for('need_confirm_contacts'))

                    return redirect(url_for('cardhouse', id=podved))
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


class Category(View):
    def dispatch_request(self):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                param_request = {'page': '1'}
                # берем данные из файла модели
                data = category_objects_list(param_request)
                departments = listDepartsments()
                getusername = getUserName()
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                breadcrumbs = "Категория подведомственной организации"
                context = {'data': data, 'departments': departments, 'getusername': getusername,
                           'breadcrumbs': breadcrumbs,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}
                print(data)


                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('category.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('category.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'category'}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class CategoryPodved(View):
    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                cat_code = request.args.get('cat_code')
                id = int(id)
                param_request = {'page': id,
                                 'cat_code': cat_code}
                page = param_request["page"]
                # берем данные из файла модели
                data = podved_list(param_request)['list_PD']
                page_info = podved_list(param_request)['Page_info']
                max_page = int(page_info['NumberOfPages'])
                pageNumber1C = int(page_info['PageNumber'])
                departments = listDepartsments()
                getusername = getUserName()
                id_podved = cat_code
                name_category_breadcrumbs = request.args.get('name')
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                breadcrumbs = "Категория подведомственной организации"
                context = {'data': data,
                           'departments': departments,
                           'getusername': getusername,
                           'page': page, 'max_page': max_page, 'pageNumber1C': pageNumber1C,
                           'namebreadcrumbsbycat': name_category_breadcrumbs,
                           'breadcrumbs': breadcrumbs,
                           'id_podved': id_podved,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments
                           }
                print(context)


                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('podved.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('podved.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'category_podved', 'id': id}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class Departament(View):
    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                print('valid')
                id = int(id)
                department = request.args.get('department')
                param_request = {'page': id, 'department': department}
                page = param_request["page"]
                # берем данные из файла модели
                data = podved_list(param_request)['list_PD']
                page_info = podved_list(param_request)['Page_info']
                max_page = int(page_info['NumberOfPages'])
                pageNumber1C = int(page_info['PageNumber'])
                departments = listDepartsments()
                getusername = getUserName()
                departid = department
                name_depart = request.args.get('value')
                breadcrumbs = "Категория подведомственной организации"
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'data': data,
                           'departments': departments,
                           'getusername': getusername,
                           'name_depart': name_depart,
                           'departid': departid,
                           'page': page, 'max_page': max_page, 'pageNumber1C': pageNumber1C,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}
                # print(response.headers)
                print(context)


                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('podved.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
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


class Cardhouse(View):
    methods=["GET"]

    def dispatch_request(self, id):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                param_request = {'code': id}
                print(id)
                # берем данные из файла модели
                data = podved_card(param_request)
                departments = listDepartsments()
                getusername = getUserName()
                id_podved = request.args.get('id_podv')
                id_podved_name = request.args.get('namebreadcrumbsbycat')
                departId = request.args.get('departments')
                departName = request.args.get('departmentsname')
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'data': data,
                           'id': id,
                           'departments': departments,
                           'getusername': getusername,
                           'id_podved': id_podved,
                           'id_podved_name': id_podved_name,
                           'departId': departId,
                           'departName': departName,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments
                           }
                print(data)


                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('cardhouse.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('cardhouse.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'cardhouse', 'id': id}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class Cardhousedetail(View):
    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        # global foto_scan
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                param_request = {'code': id}
                # берем данные из файла модели
                data = object_card(param_request)
                object_type_val = data['object_type']
                data_params = data_params_request()
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
                namedepartpodved = request.args.get('namedepartpodved')
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'data': data,
                           'object_type_val': object_type_val,
                           'id': id,
                           'data_params': data_params,
                           'departments': departments,
                           'getusername': getusername,
                           'breadcrumbs_customers': breadcrumbs_customers,
                           'idpodv': idpodv,
                           'namepodv': namepodv,
                           'idcat_podved': idcat_podved,
                           'idcat_podvedname': idcat_podvedname,
                           'namepodved': namepodved,
                           'departId': departId,
                           'departname': departname,
                           'iddepartpodved': iddepartpodved,
                           'namedepartpodved': namedepartpodved,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}
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
                                    'PurposeObject': PurposeObject, 'Condition': Condition,
                                    'technicalFloor': technicalFloor,
                                    'Lift': Lift, 'remontDate': remontDate, 'SecurityObligation': SecurityObligation,
                                    'region': region, 'address': address,
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
                    headers_get = getAccessToken()
                    headers = {'AccessToken': headers_get}
                    responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card",
                                                 data=post_request, headers=headers,
                                                 verify=False)
                    # print("response.json:\n{}\n\n".format(responsePost.json()))
                    print("response.text:\n{}\n\n".format(responsePost.text))
                    return redirect(url_for('cardhousedetail', id=id))

                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('cardhousedetail.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('cardhousedetail.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'cardhousedetail', 'id': id}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class Customers(MethodView):
    methods = ["GET", "POST"]

    def dispatch_request(self,id):
        global foto_main_thumbnail
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            print(valid)
            if valid == 'True':
                id = int(id)
                filter = request.args.get('filter')
                sort = request.args.get('sort')
                param_request = {'page': id, 'filter': filter, 'sort': sort}
                page = param_request["page"]
                # берем данные из файла модели
                data = objects_list(param_request)['list_OC']
                page_info = objects_list(param_request)['Page_info']
                print(page_info)
                max_page= int(page_info['NumberOfPages'])
                pageNumber1C= int(page_info['PageNumber'])

                # form = ObjectListForm()
                print(page, param_request)
                print(data)
                # парсинг валидации и тех даных
                data_params = data_params_request()
                departments = listDepartsments()
                getusername = getUserName()
                breadcrumbs = "Объекты недвижимости"
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'data': data, 'data_params': data_params,
                           'page': page, 'max_page':max_page,'pageNumber1C':pageNumber1C,
                           'departments': departments,
                           'getusername': getusername,
                           'breadcrumbs': breadcrumbs,
                           'filter': filter,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}
                # print(context)
                if request.method == 'POST':
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
                    print('description:', description)
                    print('object_type:', object_type)
                    print('PurposeObject:', PurposeObject)
                    print('Condition', Condition)
                    print('technicalFloor', technicalFloor)
                    print('Lift', Lift)
                    print('remontDate', remontDate)
                    print('SecurityObligation', SecurityObligation)
                    print('region:', region)
                    print('address:', address)
                    print('remontDate:', remontDate)
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
                    #     print('проблема',request.url)
                    #     return redirect(request.url)
                    foto_main = request.files['formFile']
                    name, __ = os.path.splitext(foto_main.filename)
                    text = translit(name, language_code='ru', reversed=True)
                    foto_main.filename = text+__
                    # Если файл не выбран, то браузер может
                    # отправить пустой файл без имени.

                    if foto_main.filename == '':
                        print('название фото не может быть пустым', foto_main)

                    if foto_main and allowed_file(foto_main.filename):

                        # безопасно извлекаем оригинальное имя файла
                        filename = secure_filename(foto_main.filename)

                        # сохраняем файл
                        foto_main.save(os.path.join(config.UPLOAD_FOLDER, filename))
                        foto_main = "%s/%s" % (config.UPLOAD_FOLDER, filename)
                        image = Image.open(foto_main)
                        image.thumbnail((400, 400))
                        image.save(os.path.join(config.UPLOAD_FOLDER_THUMBNAIL, filename))
                        foto_main_thumbnail = "%s/%s" % (config.UPLOAD_FOLDER_THUMBNAIL, filename)
                        print(foto_main_thumbnail)
                        print(foto_main)

                    # # загрузка мультифото
                    # if 'files[]' not in request.files:
                    #     flash('No file part')
                    #     return redirect(request.url)
                    files = request.files.getlist('files[]')
                    foto_list = []
                    foto_thumbnails_list = []
                    for file in files:
                        name, __ = os.path.splitext(file.filename)
                        text = translit(name, language_code='ru', reversed=True)
                        file.filename = text + __
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(config.UPLOAD_FOLDER_MULTI, filename))
                            image = Image.open(os.path.join(config.UPLOAD_FOLDER_MULTI, filename))
                            image.thumbnail((400, 400))
                            image.save(os.path.join(config.UPLOAD_FOLDER_MULTI_THUMBNAIL, filename))
                            foto_list.append("%s/%s" % (config.UPLOAD_FOLDER_MULTI, filename))
                            foto_thumbnails_list.append("%s/%s" % (config.UPLOAD_FOLDER_MULTI_THUMBNAIL, filename))
                    foto_multi = foto_list
                    foto_multi_thumbnails = foto_thumbnails_list
                    print(foto_multi)
                    post_request = {'name': name, 'description': description, 'object_type': object_type,
                                    'PurposeObject': PurposeObject, 'Condition': Condition,
                                    'technicalFloor': technicalFloor,
                                    'Lift': Lift, 'remontDate': remontDate, 'SecurityObligation': SecurityObligation,
                                    'region': region, 'address': address,
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
                                    'foto_main': foto_main,
                                    # 'foto_main_thumbnail': foto_main_thumbnail,
                                    'foto_multi': foto_multi,
                                    # 'foto_multi_thumbnails': foto_multi_thumbnails,
                                    'code': 'new_object'
                                    }
                    print(post_request)
                    headers_get = getAccessToken()
                    headers = {'AccessToken': headers_get}
                    responsePost = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card",
                                                 data=post_request, headers=headers,
                                                 verify=False)
                    # responsePost.encoding = "ANSI"
                    id = responsePost.json()['code']
                    print(id)
                    print("response:\n{}\n\n".format(responsePost))
                    print("response.encoding:\n{}\n\n".format(
                        responsePost.encoding))  # Узнать, какую кодировку использует Requests
                    print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
                    print("response.json:\n{}\n\n".format(responsePost.json()))
                    print(responsePost.text)
                    # context = {'id': id}
                    # return render_template('cardhousedetail/id.html')
                    return redirect(url_for('cardhousedetail', id=id))

                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('customers.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('customers.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'customers', 'id': id}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class Search(View):
    def dispatch_request(self):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                # headers_get = getAccessToken()
                # headers = {'AccessToken':headers_get}
                print(url_for('search'))
                departments = listDepartsments()
                getusername = getUserName()
                breadcrumbs = "Поиск"
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'departments': departments, 'getusername': getusername, 'breadcrumbs': breadcrumbs,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}

                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('search.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('search.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'search'}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class Reports(View):
    def dispatch_request(self):
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
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'departments': departments, 'getusername': getusername, 'breadcrumbs': breadcrumbs,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}

                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('reports.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('reports.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'category_podved', 'id': id}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


class About(View):
    def dispatch_request(self):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                print(url_for('about'))
                departments = listDepartsments()
                getusername = getUserName()
                breadcrumbs = "О проекте"
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'departments': departments, 'getusername': getusername, 'breadcrumbs': breadcrumbs,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}

                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('about.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('about.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'about'}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))


class Contacts(View):
    def dispatch_request(self):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            if valid == 'True':
                print(url_for('contacts'))
                departments = listDepartsments()
                getusername = getUserName()
                breadcrumbs = "Контакты"
                permission_menu = auth.getPermissions()
                Permission_SeeCategoryPodved = permission_menu['Permission_SeeCategoryPodved']
                Permission_SeeDepartments = permission_menu['Permission_SeeDepartments']
                # 'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved, 'Permission_SeeDepartments': Permission_SeeDepartments
                context = {'departments': departments, 'getusername': getusername, 'breadcrumbs': breadcrumbs,
                           'Permission_SeeCategoryPodved': Permission_SeeCategoryPodved,
                           'Permission_SeeDepartments': Permission_SeeDepartments}

                c = auth.getPodved()
                podved = c[0]
                permission_see = c[1]
                print(type(podved), type(permission_see))
                need_confirm_contacts = auth.updatePodvedInfo()
                if permission_see == True:
                    return render_template('contacts.html', **context)
                elif permission_see == False and need_confirm_contacts == True:
                    return redirect(url_for('need_confirm_contacts'))
                else:
                    return render_template('contacts.html', **context)
            else:
                return deleteTokens()
        elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            link_send_to_refresh = {'link': 'contacts'}
            refresh = refreshAccesToken(link_send_to_refresh)
            return refresh
        elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
            print('шляпа2')
            return deleteTokens()
        elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
            return redirect(url_for('auth_func.login'))
        else:
            return deleteTokens()


# @app.route('/region')
# @app.route('/region/')
# def region():
#     if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
#         valid = validateAccesToken()
#         if valid == 'True':
#             # print('valid')
#             # url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
#             # # if key doesn't exist, returns None
#             # param_request = {'page': '1',
#             #                  'cat_code': id}
#             # # response = requests.get(url, verify=False)
#             # response = requests.post(url, param_request, verify=False)
#             # # page = request.args.get('page', 1 ,type=int)
#             # # response = requests.get(url, verify=False)
#             #
#             # if response.status_code == 200:
#             #     print('Success!')
#             # elif response.status_code == 401:
#             #     print('Not auth.')
#             # data = response.json()['list_PD']
#             # context = {'data': data}
#             # print(data)
#             # jsonPars()
#             return render_template('future_template.html')
#         else:
#             return deleteTokens()
#     elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
#         link_send_to_refresh = {'link':'category_podved','id':id}
#         refresh = refreshAccesToken(link_send_to_refresh)
#         return refresh
#     elif not request.cookies.get('refresh_token') and request.cookies.get('access_token'):
#         print('шляпа2')
#         return deleteTokens()
#     elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
#         return redirect(url_for('auth_func.login'))
#     else:
#         return deleteTokens()
# -------------------------------------------------------------------
# Обработчики, потом их кинуть в отдельный файл.
class CheckContacts(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        getusername = getUserName()
        c = auth.getPodved()
        id = c[0]
        param_request = {'code': id}
        data = podved_card(param_request)
        print(f'параметры подведа{data}')
        contact_name = data['podved_info']['contact_name']
        contact_phone = data['podved_info']['contact_phone']
        supervisor_name = data['podved_info']['supervisor_name']
        supervisor_phone = data['podved_info']['supervisor_phone']
        context = {
            'contact_name': contact_name, 'contact_phone': contact_phone,
            'supervisor_name': supervisor_name, 'supervisor_phone': supervisor_phone,
            'getusername': getusername,
        }
        if request.method == 'POST':
            contact_name = request.form.get('contact_name')
            contact_phone = request.form.get('contact_phone')
            supervisor_name = request.form.get('supervisor_name')
            supervisor_phone = request.form.get('supervisor_phone')
            post_request = {'contact_name':contact_name,'contact_phone':contact_phone,
                            'supervisor_name':supervisor_name,'supervisor_phone':supervisor_phone}
            print(post_request)
            headers_get = getAccessToken()
            headers = {'AccessToken': headers_get}
            responsePost = requests.patch("https://localhost/copy_1/hs/HTTP_SERVER/podved_card",
                                         data=post_request, headers=headers,
                                         verify=False)
            # print("response.json:\n{}\n\n".format(responsePost.json()))
            print("response.text:\n{}\n\n".format(responsePost.text))
            # print("response:\n{}\n\n".format(responsePost))
            # print("response.url:\n{}\n\n".format(responsePost.url))  # Посмотреть формат URL (с параметрами)
            print("response.headers:\n{}\n\n".format(responsePost.headers))  # Header of the request
            print("response.status_code:\n{}\n\n".format(responsePost.status_code))  # Получить код ответа
            # print("response.text:\n{}\n\n".format(responsePost.text))  # Text Output
            # print("response.json:\n{}\n\n".format(responsePost.json()))
            # print("response.encoding:\n{}\n\n".format(responsePost.encoding))  # Узнать, какую кодировку использует Requests
            # print("response.content:\n{}\n\n".format(responsePost.content))  # В бинарном виде
            return redirect(url_for('podved', id = '1'))
        return render_template('basic/redirectpodved.html', **context)