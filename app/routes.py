from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import Admin, Coffe
from app.forms import LoginForm, RegisterForm


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = Admin.query.filter_by(email=loginform.email.data).first()
        if user is None or not user.check_password(loginform.password.data):
            flash("Username atau Password salah", "danger")
            return redirect(url_for('login'))
        flash("Login Berhasil!", "success")
        login_user(user)
        return redirect(url_for('index'))
    return render_template('sign.html', title='login', form=loginform)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        errorT = 0
        emails = [email[0] for email in db.session.query(Admin.email).all()]
        validasi_form = {
            'username': (form.username.data, 4, 64, "Nama Lengkap tidak valid"),
            'telp': (form.telp.data, 10, 15, "Nomor Telepon tidak valid"),
            'alamat': (form.alamat.data, 4, 64, "Alamat tidak valid"),
            'email': (form.email.data, 4, 45, "Email tidak valid"),
            'password': (form.password.data, 6, 45, "Password tidak valid")
        }
        for field, (data, min_len, max_len, pesan) in validasi_form.items():
            if len(data) < min_len or len(data) > max_len:
                flash(pesan, "danger")
                errorT += 1
                
        if form.email.data in emails:
            flash("Email telah terdaftar, gunakam email yang lain atau login", "danger")
            return redirect(url_for('register'))
        if errorT > 0:
            return redirect(url_for('register'))
        try:
            newUser = Admin(
                username=form.username.data,
                telp=form.telp.data,
                alamat=form.alamat.data,
                email=form.email.data,
                role="biasa"
            )
            newUser.set_password(form.password.data)
            db.session.add(newUser)
            db.session.commit()
            flash("Akun berhasil dibuat", "success")
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash("Terjadi Kesalahan", "danger")
            return redirect(url_for('register'))
    return render_template('register.html', title='register', form=form)


@app.route('/', methods=['GET','POST'])
@login_required
def index():
    menu = Coffe.query.all()
    print(menu)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        session['data_checkout'] = data
        return jsonify({"status": "Data received", "data": data}), 200
        # return redirect(url_for('checkout'))
    return render_template('index.html', title='index', menu=menu, len=len)


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', title='cart')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='profile')


@app.route("/checkout")
def checkout():
    data = session.get('data_checkout')
    pesanan = {}
    total = 0
    for isi in data:
        print(f"id: {isi}: jumlah: {data[isi]}")
        menu = Coffe.query.filter_by(id=isi).first()
        total_harga = int(data[isi]) * menu.harga 
        total += total_harga
        pesanan[menu.nama] = [data[isi], "{:,.0f}".format(total_harga).replace(",", ".")]
    print(pesanan)
    total = "{:,.0f}".format(total).replace(",", ".")
    return render_template('chekout.html', title='checkout', pesanan=pesanan, total=total)