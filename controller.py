import sqlite3 as sql
from model import *
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash, session

app = Flask(__name__)

###############################REGISTRATION.HTML##########################################
#register
@app.route('/registration')
def reg():
    return render_template('registration.html')
#login
@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('registration.html')
    else:
        return render_template('home_teacher.html')

@app.route('/login', methods=['POST'])
def dologin():
    if checklogin(request.form['teacher_id'],request.form['teacher_password']):
        session['logged_in']=True
        return redirect('/teacher')
        #users=login()
        return render_template ('home_teacher.html', users=users)
    else:
        flash('wrong password!')
        #return render_template('loginnew.html')
        return redirect('/registration')
################################home_teacher.HTML###############################################
#homepage for teacher
@app.route('/teacher')
@login_required
def ht():
    users=show_teacher()
    return render_template('home_teacher.html', users=users)

###############################REGISTRATION.HTML##########################################
@app.route("/register2", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        teacher_id = request.form.get("teacher_id")
        teacher_email = request.form.get("teacher_email")
        teacher_password = request.form.get("teacher_password")
        #teacher_password = request.form.get("teacher_password")
        register_try(teacher_email, teacher_password, teacher_id)
        return render_template("registration.html")

        if teacher_id not in users:
            users[teacher_id] = (teacher_id, teacher_password)
            return redirect(url_for("/teacher"))
        else:
            flash ('please fill out the form!', "warning")
            return render_template("registration.html")



    #logout
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        #return redirect('/')
        return render_template("index.html")

###############################LOGIN.HTML##########################################
#log_in function
#@app.route("/login", methods=['GET', 'POST'])
#def login():
    #if request.method =="POST":
        #teacher_id = request.form.get("teacher_id")
        #teacher_password = request.form.get ("teacher_password")
        #next_url = request.form.get("next")

        #if teacher_id in users and users[teacher_id][1] == teacher_password:
            #session["teacher_id"] = teacher_id
            #if next_url:
                #return redirect(next_url)
            #else:
                #return redirect(url_for("profile"))
        #else:
            #return render_template('registration.html')

######################################LOGIN.HTML##########################################
#login
#@app.route('/login', methods=['POST'])
#def login():
    #if checklogin(request.form['teacher_id'],request.form['teacher_password']):
        #session['logged_in'] = True
        #users = checklogin(request.form['teacher_id'],request.form['teacher_password'])
        #return redirect('/teacher')
        #return render_template('home_teacher.html',users=users)
    #else:

        #flash("wrong password", "danger")
        #return render_template('registration.html')
        #return redirect('/')

################################PROFILE_TEACHER.HTML###############################################
#TEACHER'S PROFILE
@app.route('/profile')
@login_required
def profile2():
    users=show_profile()
    return render_template('profile_t.html', users=users)


#edit
#@app.route('/edit/<teacher_id>')
#@login_required
#def edit(username):
        #row = find_patient (username)
        #status='1'
        #return render_template('profile_t.html',users=users,status=status)

@app.route('/edit_teacher', methods=['POST'])
def edit_teacher():

    if request.method == "POST":
        teacher_id = request.form['teacher_id']
        teacher_name = request.form['teacher_name']
        teacher_email = request.form['teacher_email']
        teacher_gender = request.form['teacher_gender']
        teacher_phone = request.form['teacher_phone']
        teacher_password = request.form['teacher_password']
        teacher_bio = request.form['teacher_bio']
        #teacher_avatar = request.form['teacher_avatar']
        edit_profile2(teacher_name, teacher_email, teacher_gender, teacher_phone, teacher_password, teacher_bio, teacher_id)
        flash("profile has been updated successfully")
        #return redirect(url_for("/profile"))
        #return redirect(request.url)
        return redirect('/profile')
    #return render_template("profile_t.html", users=users)
##################################INDEX.HTML##############################################

#home
@app.route('/')
def index():
    return render_template('index.html')

################################CAMERA.HTML###############################################
@app.route('/camera')
def cam():
    return render_template('camera2.html')

@app.route('/camera1')
def cam2():
    return render_template('camera_desktop.html')
################################PROFILE.HTML###############################################
#teacher/admin profile
#@app.route('/profile/<teacher_id>')
#@login_required
#def user(teacher_id):
    #user = teacher_login(teacher_id)
    #return render_template('profile_teacher.html', users=users)

################################PLANT BODY.HTML###############################################
#plant_body
@app.route('/plant_body')
def pb():
    return render_template('plant_body.html')

##################################KNOWME.HTML##################################################
#KNOW-ME USER VIEW
@app.route('/know_me')
def km():
    rows=knowme()
    return render_template ('know_me.html', rows=rows)
################################################################################################

################################Know_me/tree/.HTML##############################################
@app.route('/tree/<plant_id>')
#@login_required
def p0(plant_id):
    rows = tree_plant(plant_id)
    items=tree_photo(plant_id)
    return render_template('tree.html', rows=rows, items=items )
################################End Know_me/tree/.HTML##########################################

###########################CRUD IN KNOW_ME_TEACHER (table).HTML################################
#KNOW-ME-ADMIN(TEACHER) VIEW
@app.route('/know_me_teacher')
@login_required
def knowme_teacher():
    items=knowme_teach()
    return render_template ('know_me_teacher.html', items=items)

#DELETE plant_id
@app.route('/deleted/<plant_id>')
def deleted (plant_id):
    delete_plant(plant_id)
    return redirect ('/know_me_teacher')

#ADD NEW plant_id
@app.route('/adds', methods = ['POST'])
def adds ():

        if request.method == "POST":
            flash("data inserted successfully")

            plant_id = request.form['plant_id']
            plant_name = request.form['plant_name']
            plant_description = request.form['plant_description']
            plant_habitat = request.form['plant_habitat']
            plant_character = request.form['plant_character']
            plant_fact = request.form['plant_fact']
            #photo_id = request.form['photo_id']
            add_plant(plant_id, plant_name, plant_description, plant_habitat, plant_character, plant_fact )
            return redirect('/know_me_teacher')

#UPDATE/EDIT Plant
@app.route('/updated', methods = ['GET', 'POST'])
def updateds ():

        if request.method == "POST":
            plant_id = request.form['plant_id']
            plant_name = request.form['plant_name']

            plant_description = request.form['plant_description']
            plant_habitat = request.form['plant_habitat']
            plant_character = request.form['plant_character']
            plant_fact = request.form['plant_fact']
            update_plant(plant_name, plant_description, plant_habitat, plant_character, plant_fact, plant_id)
            flash("data updated successfully")
            return redirect('/know_me_teacher')

#########################END CRUD IN KNOW_ME_TEACHER (table).HTM##########################

#################################TASK.HTML################################################
#task.html view (FOR TEACHER/ADMIN ONLY)
@app.route('/task')
@login_required
def task_teacher():
    rows = task() #ref to model.py in #task view
    return render_template ('task.html', rows=rows)

#taks_1.html
@app.route('/task(1)')
def ts():
    return render_template('task1.html')

@app.route('/task(2)')
def ts2():
    return render_template('task2.html')

#DELETE Task
@app.route('/deleteme/<task_id>')
def deleteme (task_id):
    delete_task(task_id)
    return redirect ('/task')

#ADD NEW Task
@app.route('/insert', methods = ['POST'])
def add ():

    if request.method == "POST":
        task_id = request.form['task_id']
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        task_date = request.form['task_date']
        insert_task(task_id, task_name, task_description, task_date)
        return redirect('/task')

#UPDATE/EDIT Task
@app.route('/update', methods = ['GET', 'POST'])
def update ():

    if request.method == "POST":
        task_id = request.form['task_id']
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        task_date = request.form['task_date']
        update_task(task_name, task_description, task_date, task_id)
        return redirect('/task')
################################END TASK.HTML##############################################

##################################GAME.HTML################################################
#game
@app.route('/game')

def gm():
    rows=gm_task()
    return render_template('game.html', rows=rows)

#memory_game
@app.route('/memory_game')

def gm1():
    return render_template('memory_game.html')
##################################END GAME.HTML#############################################



if __name__=='__main__':
    app.secret_key = "!mzo53678912489"
    app.run(debug=True,host='0.0.0.0', port=7000)
