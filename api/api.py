from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, jsonify
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста

from flask.views import MethodView

from auth import validateAccesToken, getPodved, deleteTokens, refreshAccesToken
from models import podved_list, objects_list
from requests_obj import data_params_request, listDepartsments, getUserName
from views import Customers

api_func = Blueprint('api_func', __name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

class UserAPI(MethodView):

    def get(self, id):
        if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
            valid = validateAccesToken()
            print(valid)
            if valid == 'True':
                id = int(id)
                filter = request.args.get('filter')
                sort = request.args.get('sort')
                param_request = {'page': id, 'filter': filter, 'sort': sort}
                number2 = param_request["page"]
                # берем данные из файла модели
                data = objects_list(param_request)
                # form = ObjectListForm()
                print(number2, param_request)
                # парсинг валидации и тех даных
                data_params = data_params_request()
                departments = listDepartsments()
                getusername = getUserName()
                breadcrumbs = "Объекты недвижимости"
                context = {'data': data, 'data_params': data_params,
                           'number2': number2,
                           'departments': departments,
                           'getusername': getusername,
                           'breadcrumbs': breadcrumbs,
                           'filter': filter}
                return jsonify(context)
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

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass




@api_func.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


