from flask_app import app
from flask import render_template ,redirect,request,flash,session,url_for
from flask_app.models.user import User
from flask_app.models.house import House
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/register/login')
def home():
    return render_template('log_reg.html')

@app.post('/register')
def register():
    if User.validate(request.form):
        pw_hash=bcrypt.generate_password_hash(request.form['password'])
        data={
            **request.form,
            'password':pw_hash
        }
        user_id=User.create(data)
        session['user_id']=user_id
        session['username']=data['first_name']
        return redirect('/dashboard')
    return redirect('/register/login')

@app.post('/login')
def login():
    user_from_db=User.get_by_email({'email':request.form['email']})
    if not user_from_db:
        flash("Email doesn't exist, try to register first","log")
        return redirect('/register/login')
    if not bcrypt.check_password_hash(user_from_db.password,request.form['password']):
        flash("Password wrong please try again.","log")
        return redirect('/register/login')
    session['user_id']=user_from_db.id
    session['username']=user_from_db.first_name
    return redirect('/dashboard')

@app.post('/logout')
def logout():
    session.clear()
    return redirect ('/')

@app.route('/admin')
def admin_dash():
    users=User.get_all_users()
    houses=House.select_houses_with_pics_not_validate()
    return render_template('admin_dashboard.html',users=users, houses=houses)

@app.route('/delete/user/<int:id>', methods=['post'])
def delete_users_(id):
    user=User.delete_user({'id':id})
    return redirect('/admin')

@app.route('/delete/house/<int:id>', methods=['post'])
def delete_houses_(id):
    house=House.delete_the_house_with_its_pictures({'id':id,'house_id':id})
    return redirect('/admin')


@app.post('/validate/house/<int:id>')
def validation_of_house(id):
    User.validate_house({'house_id':id})
    return redirect('/admin')

@app.route('/house/admin/<int:id>')
def validate_photos_for_the_house(id):
    pics=House.get_all_photos_for_one_house({'house_id':id})
    return render_template('photos_admin.html',pics=pics)

@app.post("/delete/one/photo/<int:pic_id>/<int:house_id>")
def delete_that_pic(pic_id,house_id):
    User.delete_one_photo({'id':pic_id})
    return redirect(f'/house/admin/{house_id}')