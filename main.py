from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Домашняя страница')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')