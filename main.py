from flask import Flask, url_for, request, render_template
from data import db_session

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Домашняя страница')


@app.route('/enter')
def enter():
    return render_template('enter.html', title='Страница входа')


@app.route('/registration')
def registration():
    return render_template('registration.html', title='Страница регистрации')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')
