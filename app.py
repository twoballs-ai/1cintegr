import os

from flask import Flask, render_template, Blueprint, redirect, request, url_for, make_response
from flask_cors import CORS

from api.api import api_func, CustomersAPI, PodvedAPI, CategoryAPI, CardhouseDetailAPI, LoginApi, GetAccessApi, \
    ValidateAccessApi, CardhouseAPI
from models import models_func
from requests_obj import request_func
from auth import auth_func
from views import Category, Index, About, Cardhouse, Cardhousedetail, Customers, Departament, CategoryPodved, Search, \
    Reports, Contacts, CheckContacts

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True
CORS(app)

blueprint = Blueprint('site', __name__, static_url_path='/static/site', static_folder='/mnt/disk_d/1c_media/')
app.register_blueprint(blueprint)
app.register_blueprint(auth_func)
app.register_blueprint(request_func)
app.register_blueprint(models_func)
app.register_blueprint(api_func)


@app.route('/redirect_to')
def redirect_to():
    link = request.args.get('link', '/')
    new_link = 'http://' + link
    return redirect(new_link), 301


@app.route('/coockie', methods=['GET', 'POST'])
def podvedfiltercookie():
    # filter = request.args.get('filter')
    # print(filter)
    if request.method == 'POST':
        filter = request.form.get('filter')
        print(filter)
        if filter != '':
            resp = make_response(redirect(url_for('podved', id='1')))
            resp.set_cookie('filter', filter, max_age=60*60*24*365*2)
            return resp
        elif request.form.get('delete') == 'Очистить':
            resp = make_response(redirect(url_for('podved', id='1')))
            resp.set_cookie('filter', filter, max_age=0)
            return resp
        else:
            return redirect(url_for('podved', id='1'))

    #     print(filter)
    #     if filter != '':
    #         resp = make_response(redirect(url_for('podved', id='1')))
    #         resp.set_cookie('filter', filter)
    #         return resp





        # elif:
        #     return redirect(url_for('podved', id='1'))
        # elif request.form['action'] == 'Download':
        #     return 'sdsd'






@app.route('/')
def hello():
    return redirect(url_for('podved', id = '1'))


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



app.add_url_rule("/podved/<id>/",
                 view_func=Index.as_view("podved")
                 ),
app.add_url_rule("/category/",
                 view_func=Category.as_view("category")
                 ),
app.add_url_rule("/about/",
                 view_func=About.as_view("about")
                 ),
app.add_url_rule("/cardhouse/<id>/",
                 view_func=Cardhouse.as_view("cardhouse")
                 ),
app.add_url_rule("/cardhousedetail/<id>/",
                 view_func=Cardhousedetail.as_view("cardhousedetail")
                 ),
app.add_url_rule("/customers/<id>/",
                 view_func=Customers.as_view("customers")
                 ),
app.add_url_rule("/department/<id>/",
                 view_func=Departament.as_view("department")
                 ),
app.add_url_rule("/category_podved/<id>/",
                 view_func=CategoryPodved.as_view("category_podved")
                 ),
app.add_url_rule("/search/",
                 view_func=Search.as_view("search")
                 ),
app.add_url_rule("/reports/",
                 view_func=Reports.as_view("reports")
                 ),
app.add_url_rule("/contacts/",
                 view_func=Contacts.as_view("contacts")
                 )
app.add_url_rule("/need_confirm_contacts/",
                 view_func=CheckContacts.as_view("need_confirm_contacts")
                 )

login_view = LoginApi.as_view('login_view')
app.add_url_rule('/api/v1.0/login/',
                 # defaults={'id': '1'},
                 view_func=login_view, methods=['GET',])
app.add_url_rule('/api/v1.0/login/', view_func=login_view, methods=['POST',])

acces_token = GetAccessApi.as_view('acces_token')
app.add_url_rule('/api/v1.0/access/',
                 # defaults={'id': '1'},
                 view_func=acces_token, methods=['GET',])
app.add_url_rule('/api/v1.0/access/', view_func=acces_token, methods=['POST',])

valid_acces_token = ValidateAccessApi.as_view('valid_acces_token')
app.add_url_rule('/api/v1.0/valid/',
                 # defaults={'id': '1'},
                 view_func=valid_acces_token, methods=['GET',])
app.add_url_rule('/api/v1.0/valid/', view_func=valid_acces_token, methods=['POST',])

customers_view = CustomersAPI.as_view('customers_api')
app.add_url_rule('/api/v1.0/customers/<int:id>/',
                 # defaults={'id': '1'},
                 view_func=customers_view, methods=['GET',])
app.add_url_rule('/api/v1.0/customers/post/', view_func=customers_view, methods=['POST',])
# app.add_url_rule('/users/<int:user_id>', view_func=user_view,
#                  methods=['GET', 'PUT', 'DELETE'])
podved_view = PodvedAPI.as_view('podved_api')
app.add_url_rule('/api/v1.0/podved/',
                 # defaults={'id': '1'},
                 view_func=podved_view, methods=['GET',])
category_view = CategoryAPI.as_view('category_api')
app.add_url_rule('/api/v1.0/category/',
                 # defaults={'id': '1'},
                 view_func=category_view, methods=['GET',])

cardhouse_detail_view = CardhouseDetailAPI.as_view('cardhouse_detail_api')
app.add_url_rule('/api/v1.0/cardhousedetail/<id>/',
                 # defaults={'id': '1'},
                 view_func=cardhouse_detail_view, methods=['GET',])

cardhouse_view = CardhouseAPI.as_view('cardhouse_api')
app.add_url_rule('/api/v1.0/cardhouse/<id>/',
                 # defaults={'id': '1'},
                 view_func=cardhouse_view, methods=['GET',])

if __name__ == '__main__':
    app.run(host='10.0.0.13')
    # app.run(debug=True)
