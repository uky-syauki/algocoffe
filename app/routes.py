from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import Admin, Coffe, Transaksi, Transaksi_menu
from app.forms import LoginForm, RegisterForm, PesananForm




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


@app.route('/pesanan')
@login_required
def pesanan():
    data = {}
    bayar = 0
    curr_trx = Transaksi.query.filter_by(id_user=current_user.id, status="Diproses")
    for trx in curr_trx:
        data[trx.id] = {}
        data[trx.id]['date'] = trx.date
        data[trx.id]['status'] = trx.status
        data[trx.id]["menu"] = {}
        for menu in trx.menu():
            data[trx.id]['menu'][menu.id] = {}    
            data[trx.id]['menu'][menu.id]['jumlah'] = menu.jumlah    
            pesanan = menu.pesanan()
            data[trx.id]['menu'][menu.id]['nama'] = pesanan.nama    
            data[trx.id]['menu'][menu.id]['harga'] = '{:,.0f}'.format(pesanan.harga).replace(',','.') 
            data[trx.id]['menu'][menu.id]['total'] = '{:,.0f}'.format(menu.jumlah * pesanan.harga).replace(',','.') 
            bayar += menu.jumlah * pesanan.harga
    bayar = '{:,.0f}'.format(bayar).replace(',','.')
    return render_template('cart.html', title='pesanan', data=data, bayar=bayar)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='profile')


@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    form = PesananForm()
    data = session.get('data_checkout')
    pesanan = {}
    total = 0
    for isi in data:
        print(f"id: {isi}: jumlah: {data[isi]}")
        menu = Coffe.query.filter_by(id=isi).first()
        total_harga = int(data[isi]) * menu.harga 
        total += total_harga
        pesanan[menu.nama] = [data[isi], "{:,.0f}".format(total_harga).replace(",", ".")]
    if form.validate_on_submit():
        trx = Transaksi(id_user=current_user.id)
        db.session.add(trx)
        for isi in data:
            menu = Coffe.query.filter_by(id=isi).first()
            trx_menu = Transaksi_menu(id_transaksi=trx.id, id_menu=menu.id, jumlah=data[isi])
            db.session.add(trx_menu)
        try:
            db.session.commit()
            return redirect(url_for('pesanan'))
        except:
            flash("Terjadi kesalahan", "danger")
            db.session.rollback()
    total = "{:,.0f}".format(total).replace(",", ".")
    return render_template('chekout.html', title='checkout', pesanan=pesanan, total=total, form=form)