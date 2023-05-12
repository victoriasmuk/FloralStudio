import requests 
import base64
import os
import io
from flask import render_template, request, redirect, session, url_for, flash
from flask_app import app
from PIL import Image
from flask_app.models.users_model import User
from flask_app.models.bouquets_model import Bouquet
from flask_app.models.flowers_model import Flower
from flask_app.config.config import api_key

UPLOAD_FOLDER = '/Users/victoriasmuk/Desktop/coding_dojo/FloralStudio/flask_app/static/images/uploaded_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/show_bouquets/<int:user_id>')
def show_bouquets(user_id):
    if not 'uid' in session:
        flash('Please sign in first!')
        return redirect('/login')
    bouquets = Bouquet.get_with_user(user_id)
    logged_in_user = User.get_user_by_id(session['uid'])
    return render_template('show_bouquets.html', bouquets=bouquets, user = logged_in_user)

@app.route('/get_estimate')
def get_estimate():
    if not 'uid' in session:
        flash('Please sign in first!')
        return redirect('/login')
    if 'uid' in session:
        user = session['uid']
    else:
        user = 0
    if 'image' in session:
        image = session['image']
        common_names = session['common_names']
        names = session['names'] 
    else:
        image = 0
        common_names = 0
        names = 0

    return render_template('get_estimate.html', user = user, image=image, common_names = common_names, names = names)


@app.route('/upload_photo', methods = ['POST'])
def upload_photo():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
        image = request.files['image']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path)

    session['image'] = image.filename
    ############## API STARTS HERE ##############
    with open(path,'rb') as file:
        images = [base64.b64encode(file.read()).decode("ascii")]
    response = requests.post(
        "https://api.plant.id/v2/identify",
    json={
        "images": images,
        "plant_details": ["common_names"],
    },
    headers={
        "Content-Type": "application/json",
        "Api-Key": api_key,
    }).json()

    suggestions = response["suggestions"]

    common_names = []
    names = []
    for suggestion in suggestions:
        if suggestion["plant_details"]["common_names"] is not None:
            for x in suggestion["plant_details"]["common_names"]:
                common_name = x
                common_names.append(common_name)
        plant_name = suggestion["plant_name"]
        names.append(plant_name)

    session['common_names'] = common_names
    session['names'] = names

    print(common_names)
    print(names)


    size = request.form['size']
    data = {
    "flowers" : Bouquet.find_flowers(suggestions),
    "user_id" : session['uid'],
    "bouquet_size" : size
    }
    cost = Bouquet.calculate(data)
    session['cost'] = cost
    data2 = {
        "user_id" : session['uid'],
        "size" : size,
        "price" : cost,
        "uploaded_photo" : session['image']
    }
    session['size'] = request.form['size']
    Bouquet.save(data2)
    return redirect(url_for('get_estimate'))

@app.route('/clear_estimate')
def clear_estimate():
    session.pop('image_details', default=None)
    session.pop('size', default=None)
    session.pop('image', default=None)
    session.pop('cost', default=None)
    return redirect('/get_estimate')

@app.route('/show_flowers')
def show_flowers():
    flowers = Flower.get_all()
    if 'uid' in session:
        user = session['uid']
    else:
        user = 0

    return render_template('show_flowers.html', flowers=flowers, user=user)



