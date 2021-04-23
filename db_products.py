# при запуске этого файла создаётся база данных с продуктами
from data import db_session
from data.products import Product


def add_products():
    db_sess = db_session.create_session()
    product = Product(
        name='Jeans',
        price=3000,
        path_photo='products/jeans.jpg')
    db_sess.add(product)
    product = Product(
        name='shirt',
        price=1500,
        path_photo='products/shirt.jpg')
    db_sess.add(product)
    product = Product(
        name='skirt',
        price=2000,
        path_photo='products/skirt.jpg')
    db_sess.add(product)
    product = Product(
        name='shoes',
        price=4000,
        path_photo='products/shoes.jpg')
    db_sess.add(product)
    db_sess.commit()


db_session.global_init("db/products.db", flag=True)
add_products()
