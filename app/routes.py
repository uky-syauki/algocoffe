from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.html', title='index')


@app.route('/cart')
def cart():
    return render_template('cart.html', title='cart')