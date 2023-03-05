from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, jsonify
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста

from flask.views import MethodView

from auth import validateAccesToken, getPodved, deleteTokens, refreshAccesToken
from models import podved_list, objects_list, objects_list_api, podved_list_api, category_objects_list_api, \
    object_card_api
from requests_obj import data_params_request, listDepartsments, getUserName
from views import Customers

api_func = Blueprint('api_func', __name__)


class CustomersAPI(MethodView):

    def get(self, id):
        id = id

        param_request = {'page': id}
        # берем данные из файла модели
        data = objects_list_api(param_request)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class PodvedAPI(MethodView):

    def get(self):


        param_request = {'page': '1'}
        # берем данные из файла модели
        data = podved_list_api(param_request)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class CategoryAPI(MethodView):

    def get(self):
        param_request = {'page': '1'}
        # берем данные из файла модели
        data = category_objects_list_api(param_request)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class CardhouseDetailAPI(MethodView):

    def get(self,id):
        param_request = {'code': id}
        # берем данные из файла модели
        data = object_card_api(param_request)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

