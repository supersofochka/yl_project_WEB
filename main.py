from flask import Flask, url_for, request, render_template, redirect
from data import db_session
from forms.user import RegisterForm, EnterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
    return 'Продукты'


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')
