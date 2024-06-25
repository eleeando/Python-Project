from flask_app import app, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import render_template ,redirect,request,flash,session
from flask_app.models.house import House

import os
from werkzeug.utils import secure_filename
import uuid

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/buy/house')
def get_houses_for_sale():
    houses=House.select_all_houses_for_sale_with_pic()
    return render_template('all_houses_for_sale.html',houses=houses)


@app.route('/sell/house')
def put_a_house_to_sell():
    return render_template('create_a_house_to_sell.html')

@app.post('/create/house/sell')
def sell_the_house():
    data={
        'user_id':session['user_id'],
        **request.form
    }
    
    new_house_id=House.create_a_house(data)
    return redirect('/house/pics_forhouse/'+str(new_house_id))

@app.post('/house/pics/insert')
def insert_pics_to_the_house_to_sell():
    print("IMAGE FORM-----",request.form)
    print("IMAGE FiLE-----",request.files)
    file = request.files['path']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate a UUID for the filename
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file.save(os.path.join(UPLOAD_FOLDER, unique_filename))

        data = {
            **request.form,
            'path': unique_filename
        }
        House.put_photos_for_the_house(data)
    return redirect(f'/house/pics_forhouse/{request.form['house_id']}')

@app.route('/house/confirm', methods=['post'])
def confirm_house():
    id  = request.form['id']
    return redirect(f'/house/{int(id)}')

@app.route('/house/pics_forhouse/<int:id>')
def get_house_by_id(id):
    pics=House.get_all_photos_for_one_house_id({'house_id':id})
    return render_template('on_house.html', data=id ,pics=pics)


@app.route("/rent/house")
def house_rent():
    houses=House.select_all_houses_for_rent_with_pic()
    return render_template('all_houses_for_rent.html',houses=houses)

@app.route("/mortgage/house")
def mortgage():
    houses=House.select_all_houses_for_mortgage_with_pic()
    return render_template('all_houses_for_mortgage.html',houses=houses)


@app.route("/house/<int:id>")
def one_house(id):
    home=House.select_one_house_with_owner({'id':id})
    pics=House.get_all_photos_for_one_house({'house_id':id})
    print(pics)
    return render_template('one_house.html', house=home, pics=pics)



@app.post('/delete/photo/<int:id>')
def deletion(id):
    House.delete_on_pic({'id':id})
    return redirect(f'/house/pics_forhouse/{request.form['house_id']}')

@app.route('/creteria/house')
def creteria():
    return render_template('choose_criteria.html')

@app.post("/choose")
def choose():
    houses=House.select_houses_with_crita(request.form)
    return render_template('all_houses_for_mortgage.html',houses=houses)






@app.route('/my_house/<int:id>')
def myhouses(id):
    houses=House.get_my_houses({'user_id':id})
    return render_template('my_houses.html',houses=houses)