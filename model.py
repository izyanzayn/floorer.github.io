import sqlite3 as sql
from functools import wraps
from flask import session, flash, redirect, url_for, request
#####################################################################################################
connect_db = 'identime.db'
#####################################################################################################
#know-me view
#@app.route('/know_me')
def knowme():
    with sql.connect(connect_db) as db:
        qry = 'select know_me.plant_name,know_me.plant_id from know_me'
        result = db.execute(qry)
        return (result)

        def result():
            rows = knowme()
            for row in rows:
                print (row)
#####################################################################################################

#####################################################################################################
#know-me admin/teacher view
#@app.route('/know_me_teacher')
def knowme_teach():
    with sql.connect(connect_db) as db:
        qry = 'select know_me.plant_id, know_me.plant_name, know_me.plant_description, know_me.plant_habitat, know_me.plant_character, know_me.plant_fact from know_me'
        result = db.execute(qry)
        return (result)

        def result():
            items = knowme_teach()
            for item in items:
                print (item)

#DELETE plant_id
def delete_plant (plant_id):
    with sql.connect(connect_db) as db:
        qry='delete from know_me where plant_id=?'
        db.execute(qry,(plant_id,))

#ADD NEW plant_id
def add_plant(plant_id, plant_name, plant_description, plant_habitat, plant_character, plant_fact):
    with sql.connect(connect_db) as db :
        qry='insert into know_me values (?,?,?,?,?,?)'
        db.execute (qry, (plant_id, plant_name, plant_description, plant_habitat, plant_character, plant_fact))

#UPDATE/EDIT plant_id
def update_plant (plant_name, plant_description, plant_habitat, plant_character, plant_fact, plant_id):
    with sql.connect (connect_db) as db:
        qry='update know_me set plant_name=?, plant_description=?, plant_habitat=?, plant_character=?, plant_fact=? where plant_id=?'
        db.execute(qry, (plant_name, plant_description, plant_habitat, plant_character, plant_fact, plant_id))
#####################################################################################################

#####################################################################################################
#tree view
#@app.route('/tree/(plant name)')
def tree_plant(plant_id):     ##
    with sql.connect(connect_db) as db:
        qry = """select know_me.plant_name, know_me.plant_description, know_me.plant_habitat, know_me.plant_character, know_me.plant_fact from know_me where plant_id='%s'"""% (plant_id)
        #qry="""select * from know_me inner join photo on know_me.plant_id = photo.plant_id where know_me.plant_id=='%s'"""% (plant_id)
        #qry='select * from know_me inner join photo on know_me.plant_id = photo.plant_id'
        result = db.execute(qry).fetchmany()
        return (result)

        def result():
            rows = tree_plant() ##
            for row in rows:
                print (row)


#photo
def tree_photo(plant_id):     ##
    with sql.connect(connect_db) as db:
        #qry = 'select * from photo'
        #qry = """select * from photo where photo_id =?"""
        qry="""select photo_path from photo inner join know_me on photo.plant_id = know_me.plant_id where know_me.plant_id=='%s'"""% (plant_id)
        result = db.execute(qry)
        return (result)

    def result():
        items = tree_photo() ##
        for item in items:
            print (item)


#########################################################################################################
#@app.route('/game')
#_show_task
def gm_task():
    with sql.connect(connect_db) as db:
        qry = 'select task.task_name, task.task_description from task'
        result = db.execute(qry)
        return (result)

        def result():
            rows = gm_task()
            for row in rows:
                print (row)
#########################################################################################################
#TASK.html CRUD
#task view
def task():
    with sql.connect(connect_db) as db:
        qry = 'select * from task'
        result = db.execute(qry)
        return (result)

def result():
    rows = task()
    for row in rows:
        print (row)

#DELETE Task
def delete_task (task_id):
    with sql.connect(connect_db) as db:
        qry='delete from task where task_id=?'
        db.execute(qry,(task_id,))

#ADD NEW Task
def insert_task(task_name, task_description, task_date, task_id):
    with sql.connect(connect_db) as db :
        qry='insert into task values (?,?,?,?)'
        db.execute (qry, (task_name, task_description,task_date, task_id))

#UPDATE/EDIT Task
def update_task (task_name, task_description, task_date, task_id):
    with sql.connect (connect_db) as db:
        qry='update task set task_name=?, task_description=?, task_date=? where task_id=?'
        db.execute(qry, (task_name, task_description, task_date, task_id))



#########################################################################################################

#profile_teacher.html CRUD
#teacher view only
def show_profile():
    with sql.connect(connect_db) as db:
        qry = 'select teacher.teacher_id, teacher.teacher_name, teacher.teacher_email, teacher.teacher_gender, teacher.teacher_phone, teacher_password, teacher.teacher_bio from teacher'
        result = db.execute(qry).fetchmany()
        return (result)

def result():
    users = show_profile()
    for user in users:
        print (user)

#UPDATE/EDIT Teacher
def edit_profile2(teacher_name, teacher_email, teacher_gender, teacher_phone, teacher_password, teacher_bio, teacher_id):
    with sql.connect (connect_db) as db:
        qry='update teacher set teacher_name =?, teacher_email=?, teacher_gender=?, teacher_phone=?, teacher_password=?, teacher_bio=? where teacher_id=?'
        db.execute(qry, (teacher_name, teacher_email, teacher_gender, teacher_phone, teacher_password, teacher_bio, teacher_id))

#########################################################################################################

####################################home_teacher.html#####################################################
#TEACHER-HOMEPAGE
#@app.route('/teacher')
def show_teacher():
    with sql.connect(connect_db) as db:
        #qry = """select know_me.plant_name, know_me.plant_description, know_me.plant_habitat, know_me.plant_character, know_me.plant_fact from know_me where plant_id='%s'"""% (plant_id)
        qry = 'select teacher.teacher_name,teacher.teacher_id from teacher'
        result = db.execute(qry).fetchmany()
        return (result)

        def result():
            users = show_teacher()
            for user in users:
                print (user)

#####################################################################################################
#################################LOGIN FOR TEACHER/ADMIN ONLY########################################
#login
def checklogin(teacher_id,teacher_password):
    with sql.connect (connect_db) as db:
        qry = 'select * from teacher where teacher_id=? and teacher_password =?'
        #db.execute(qry, (staff_id,password)).fetchone()
        result=db.execute(qry,(teacher_id,teacher_password )).fetchone()
        return(result)

#register
def register_try(teacher_email, teacher_password, teacher_id):
    with sql.connect(connect_db) as db :
        qry='insert into teacher (teacher_id,teacher_password,teacher_email) values (?,?,?)'
        db.execute (qry, (teacher_id,teacher_password,teacher_email))
#################################################################################################
#################################################################################################
#helper function
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else :
            flash("You need to login first", "danger")
        return redirect(url_for('/teacher'))
    return wrap
#end login
