from flask import Flask, render_template, redirect, request
from data import db_session
from forms.user import RegisterForm, EnterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

result = 0


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Домашняя страница')


@app.route('/enter', methods=['GET', 'POST'])
def enter():
    form = EnterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('enter.html', title='Регистрация',
                                   form=form,
                                   message="Нет такого пользователя")
        if not user.check_password(form.password.data):
            return render_template('enter.html', title='Регистрация',
                                   form=form,
                                   message="Неверный пароль")
        return redirect('/products')
    return render_template('enter.html', title='Вход', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/enter')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/products')
def products():
    return render_template('products.html', title='Каталог')


@app.route('/basket', methods=['POST', 'GET'])
def basket():
    global result

    if request.method == 'GET':
        return render_template('basket.html', title='Корзина')

    elif request.method == 'POST':
        if request.form['jeans']:
            if int(request.form['jeans']) > 0:
                result += int(request.form['jeans']) * 3000

        if request.form['shirt']:
            if int(request.form['shirt']) > 0:
                result += int(request.form['shirt']) * 1500

        if request.form['shoes']:
            if int(request.form['shoes']) > 0:
                result += int(request.form['shoes']) * 4000

        if request.form['skirt']:
            if int(request.form['skirt']) > 0:
                result += int(request.form['skirt']) * 2000

        return redirect('/order')


@app.route('/order', methods=['POST', 'GET'])
def order():
    if request.method == 'GET':
        return render_template('order.html', title='Заказ', sum=result)
    elif request.method == 'POST':
        return redirect('/result')


@app.route('/result')
def result_order():
    return render_template('result_order.html', title='Готово!')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')
