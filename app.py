from flask import Flask, render_template, redirect, url_for, request,flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, IntegerField, FloatField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flaskext.mysql import MySQL
from sqlalchemy import create_engine
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:abduabdu@127.0.0.1:3306/dining'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

mysql = MySQL()
mysql.init_app(app)
# conn = mysql.connect()
# cursor = mysql.connection.cursor()

engine = create_engine('mysql+pymysql://abduabdu:abduabdu@34.27.20.160:3306/dining')
# engine = create_engine('mysql+pymysql://root:abduabdu@127.0.0.1:3306/dining')
connection = engine.raw_connection()
cursor = connection.cursor()

class InsertStud(FlaskForm):
    studentID = StringField(label = 'Enter the student ID:')
    studentName = StringField(label = 'Enter the name of the student:')
    studentRestriction = StringField(label = "Enter the student's dietary restriction ID")
    submitted = SubmitField(label = 'Submit')

class SearchMeal(FlaskForm):
    studentRestriction = StringField(label = 'Enter restriction ID to search:')
    submitted = SubmitField(label = 'Submit')

class UpdateName(FlaskForm):
    studentID = StringField(label = 'Enter your student ID:')
    studentName = StringField(label = 'Enter new name to update:')
    submitted = SubmitField(label = 'Submit')
    
class DeleteMeal(FlaskForm):
    studentID = StringField(label = 'Enter student ID to delete:')
    submitted = SubmitField(label = 'Submit')
    
class AdvancedQuery1(FlaskForm):
    submitted = SubmitField(label = 'Submit')
    
class AdvancedQuery2(FlaskForm):
    submitted = SubmitField(label = 'Submit')

class AdvancedDatabaseProgram(FlaskForm):
    mealID = StringField(label = 'Enter meal ID to search:')
    submitted = SubmitField(label = 'Submit')


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/insertmain.html', methods = ['GET', 'POST'])
def insert():
    insform = InsertStud()
    if insform.validate_on_submit():
        studid = insform.studentID.data
        studnm = insform.studentName.data
        studrst = insform.studentRestriction.data
        cursor.execute("INSERT INTO Student VALUES (%s, %s, %s);", (studid, studnm, studrst))
        connection.commit()
        # data = cursor.fetchall()
        return render_template('home.html')
    return render_template('insertmain.html', form = insform)
       
@app.route('/deletemain.html', methods = ['GET', 'POST'])
def delete():
            
    delform = DeleteMeal()
    if delform.validate_on_submit():
        studid = delform.studentID.data
        cursor.execute("DELETE FROM Student WHERE StudentID=%s", (studid))
        connection.commit()
        # data = cursor.fetchall()
        return render_template('home.html')
    return render_template('deletemain.html', form = delform)

@app.route('/searchmain.html', methods = ['GET', 'POST'])
def search():

    searchform = SearchMeal()
    if searchform.validate_on_submit():
        restid = searchform.studentRestriction.data
        cursor.execute("SELECT StudentID, StudentName, Restrictions FROM Student WHERE Restrictions = %s", (restid))
        connection.commit()
        data = cursor.fetchall()
        return render_template('resultsmain.html', data = data)
    return render_template('searchmain.html', form = searchform)


@app.route('/updatemain.html', methods = ['GET', 'POST'])
def update():

    updform = UpdateName()
    if updform.validate_on_submit():
        studid = updform.studentID.data
        studnm = updform.studentName.data
        cursor.execute("UPDATE Student SET StudentName = %s WHERE StudentID = %s;", (studnm, studid))
        connection.commit()
        # data = cursor.fetchall()
        return render_template('home.html')
    return render_template('updatemain.html', form = updform)

    
@app.route('/resultsq1.html', methods = ['GET', 'POST'])
def q1():
    cursor.execute("SELECT DISTINCT h.Name FROM DiningHall h NATURAL JOIN Menu WHERE MenuID IN (SELECT DISTINCT MenuID FROM DiningHall NATURAL JOIN Menu GROUP BY MenuID HAVING count(*) > 1) ORDER BY h.Name ASC LIMIT 15")
    
    # cursor.execute("SELECT DISTINCT h.Name FROM DiningHall h NATURAL JOIN Menu NATURAL JOIN Meal WHERE MealID IN (SELECT MealID FROM DiningHall NATURAL JOIN Menu NATURAL JOIN Meal GROUP BY MealID HAVING count(*) > 1) ORDER BY h.Name ASC LIMIT 15")

    connection.commit()
    data = cursor.fetchall()
    return render_template('resultsq1.html', data = data)

@app.route('/resultsq2.html', methods = ['GET', 'POST'])
def q2():
    cursor.execute("SELECT DISTINCT r.RestrictionID FROM Student s NATURAL JOIN Restriction r GROUP BY r.RestrictionID HAVING COUNT(s.StudentID) > 1 ORDER BY RestrictionID ASC LIMIT 15")
    connection.commit()
    data = cursor.fetchall()
    return render_template('resultsq2.html', data = data)

@app.route('/advdbprog.html', methods = ['GET', 'POST'])
def adbp():
    advprogform = AdvancedDatabaseProgram()
    if advprogform.validate_on_submit():
        mealid = advprogform.mealID.data

        out = 0
        
        cursor.callproc('checkForRemovableMeal', [mealid, out])

        for out in cursor.stored_results():
            if out:
                data = "Yes!"
            else:
                data = "No!"

        return render_template('resultsadv.html', data = data)
    return render_template('advdbprog.html', form = advprogform)
    

# print("BEFORE")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

# print("AFTER")
