import os

from flask import Flask, render_template, Blueprint


from api.api import api_func, UserAPI
from models import models_func
from requests_obj import request_func
from auth import auth_func
from views import Category, Index, About, Cardhouse, Cardhousedetail, Customers, Departament, CategoryPodved, Search, \
    Reports, Contacts

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True

blueprint = Blueprint('site', __name__, static_url_path='/static/site', static_folder='/mnt/disk_d/1c_media/')
app.register_blueprint(blueprint)
app.register_blueprint(auth_func)
app.register_blueprint(request_func)
app.register_blueprint(models_func)
app.register_blueprint(api_func)


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


app.add_url_rule("/index/",
                 view_func=Index.as_view("index")
                 ),
app.add_url_rule("/",
                 view_func=Index.as_view("/")
                 ),
app.add_url_rule("/podved/",
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

user_view = UserAPI.as_view('user_api')
app.add_url_rule('/api/v1.0/customers/<id>/', defaults={'id': 1},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])


if __name__ == '__main__':
    app.run(host='10.0.0.13')
    # app.run(debug=True)
