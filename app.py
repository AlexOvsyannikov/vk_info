from flask import Flask, render_template, flash, redirect, request
from forms import VK_LINK
from func import get_id
from make_database import *
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods = ['GET', 'POST'])
def index():
    print(request.remote_addr)

    form = VK_LINK()
    if form.validate_on_submit():
        print(form.vk_link.data)
        return redirect('/id'+str(get_id(form.vk_link.data)))

    return render_template('index.html',
                           Title="VK-Parser",
                           form=form)
@app.route('/id<id>')
def hi(id):
    if id == "Error":
        return "Error"

    fileway = write_info(users_get(id))
    with open(fileway+"/info.txt","r") as f:
        data=f.readlines()

    fileway=fileway.split("/")[-1]
    img_path="/database/"+fileway+"/photo.jpg"

    return render_template("data.html",
        Title = id,
        img_path = img_path,
        data=data
    )

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return redirect("https://oauth.vk.com/authorize?client_id=7616557&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=336902&response_type=code&v=5.124")

if __name__ == '__main__':
    app.run()
