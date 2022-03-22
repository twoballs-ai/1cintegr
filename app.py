from flask import Flask, render_template, url_for, request

app = Flask(__name__)
app.debug =True
app.config['SECRET_KEY'] = 'cdvfdjn43439acd9*&^$%&*&^%G&^%FGYH'


@app.route('/')
@app.route('/index')
def index():
    print(url_for('index'))
    return render_template('index.html', title='minkult-CRM')


# пример создания ссылок
# @app.route('/url/<int:variable>/<variable>')


# роверка ссылок на правильность
# with app.test_request_context():
#     print(url_for('index'))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page_404.html', title='страница не найдена'),404


if __name__ == '__main__':
    app.run(debug=True)
