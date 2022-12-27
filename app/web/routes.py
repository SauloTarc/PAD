from flask import Blueprint, render_template, redirect, flash, request, current_app
from app import db
from ..controllers.wtforms import (AddressForm, PostForm,
                                   SignUpForm, LoginForm,
                                   ProfileForm)
from flask_login import login_user, current_user, logout_user, login_required
from ..models.model import Address, ProfileType, User, Post, Profile
import os
import secrets
from PIL import Image


bp = Blueprint('bp', __name__, template_folder='template', static_folder='static')

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.pub_date.desc()).paginate(page=page, per_page=6)
    return render_template('index.html', posts=posts)


@bp.route('/signup', methods=['GET', 'POST'])
def signup(): 
    
    if current_user.is_authenticated:
        return redirect('/index')
    
    form = SignUpForm()
    
    try:    
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            pwd = form.password.data
            user = User(username=username, email=email, password=pwd,)
            db.session.add(instance=user)
            db.session.commit()
            return redirect('login')
    except:
        flash(message='O email informado já foi cadastrado', category='info') 
           
    return render_template('signup.html', form=form)


@bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        return redirect('index')
    except:
        return redirect('index')

   
@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect('index')
    
    form = LoginForm()
    
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        pwd = form.password.data
        
        if user:
            try:
                check_pwd = user.verify_password(pwd)
                if check_pwd:
                    login_user(user, remember=form.remember_me.data)
                    return redirect('index')
                else:
                    flash('Senha incorreta', 'danger')
                    return redirect('login')
            except:
                flash('Senha incorreta', 'danger')
                return redirect('login')
        else:
            flash(' Usuário e/ou senha incorretos', 'danger')
            return redirect('login')
            
    return render_template('login.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #Unpacking do arquivo de imagem
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/image/profile', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    form = ProfileForm()
    
    try:
        if form.validate_on_submit():
            profile_image = save_picture(form.image_file.data)
            image_file = profile_image
            institucional_name = form.institucional_name.data
            phone = form.phone.data
            cnpj = form.cnpj.data
            about = form.about.data
            profile_type = form.profile_type.data
            profile = Profile(image_file=image_file,
                            institucional_name=institucional_name,
                            phone=phone,
                            cnpj=cnpj,
                            about=about,
                            profile_type=profile_type)
            db.session.add(profile)
            db.session.commit()
            return redirect('address')
    except:
        flash(message='Algum campo está vazio ou incorreto')
        return redirect('profile')
        
    return render_template('profile.html', form=form)
    

@bp.route('/address', methods=['GET','POST'])
@login_required
def address():
    
    form = AddressForm()
    
    try:
        if form.validate_on_submit:
            city = form.city.data
            district = form.district.data
            street = form.street.data
            number = form.number.data
            address = Address(city=city, district=district, street=street, number=number)
            db.session.add(address)
            db.session.commit()
            return redirect('index')
    except:
        flash(message='Algum campo está vazio ou incorreto')
        redirect('address')
    
    return render_template('address.html', form=form)  


@bp.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    return render_template('account.html')


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm
    if form.validate_on_submit:
        title = form.title.data
        description = form.description.data