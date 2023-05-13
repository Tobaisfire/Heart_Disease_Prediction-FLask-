from flask import Flask,render_template,redirect,url_for,request,session,g,flash
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime 
import re
from admin.routes import routes
import pickle
import numpy as np


local_server = True

model = pickle.load(open('D:\keval\study\Projects\hdp\Heart_Disease_Prediction-FLask-\modal2.pkl','rb'))


app = Flask(__name__)
app.register_blueprint(routes,url_prefix='')

if (local_server == True):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hdp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#payment module code----------------------------------------------------------------------------------
from instamojo_wrapper import Instamojo

API_KEY = "test_1ad79f83a33b5de2516eaacd2a8"

AUTH_TOKEN = "test_9786a808d209aa8cc8df8a3664c"

api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')
 #---------------------------------------------------------------------------------------------------------

class Hdpuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName  = db.Column(db.String(120), unique=False,nullable = False)
    LastName  = db.Column(db.String(120), unique=False,nullable = False)
    Email  = db.Column(db.String(20), unique=False, nullable = False)
    Ph_no  = db.Column(db.Integer, unique=False, nullable = False)
    Profession  = db.Column(db.String(12), unique=False, nullable = False)
    Username  = db.Column(db.String(120), unique=False, nullable = False)
    Password  = db.Column(db.String(120), unique=False, nullable = False)
    
class Doclogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Firstname  = db.Column(db.String(120), unique=False,nullable = False)
    Lastname  = db.Column(db.String(120), unique=False,nullable = False)
    Ph = db.Column(db.Integer, unique=False, nullable = False)
    Profession=db.Column(db.String(120), unique=False, nullable = False)
    Email  = db.Column(db.String(20), unique=False, nullable = False)
    Username  = db.Column(db.String(120), unique=False, nullable = False)
    Password = db.Column(db.String(120), unique=False, nullable = False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username  = db.Column(db.String(120), unique=False, nullable = False)
    Password = db.Column(db.String(120), unique=False, nullable = False)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email =  db.Column(db.String(120), unique=False, nullable = False)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Age= db.Column(db.Integer, unique=False,nullable = False)
    Sex  = db.Column(db.Integer, unique=False,nullable = False)
    Cp  = db.Column(db.Integer, unique=False,nullable = False)
    Trestbps  =db.Column(db.Integer, unique=False,nullable = False)
    Chol  = db.Column(db.Integer, unique=False,nullable = False)
    Fbs  = db.Column(db.Integer, unique=False,nullable = False)
    Restecg  = db.Column(db.Integer, unique=False,nullable = False)
    Thalach  = db.Column(db.Integer, unique=False,nullable = False)
    Exang  = db.Column(db.Integer, unique=False,nullable = False)
    Oldpeak  = db.Column(db.Integer, unique=False,nullable = False)
    Slope  = db.Column(db.Integer, unique=False,nullable = False)
    Ca  = db.Column(db.Integer, unique=False,nullable = False)
    Thal  = db.Column(db.Integer, unique=False,nullable = False)
    Target  = db.Column(db.Integer, unique=False,nullable = False)


app.secret_key ='recordsaremeanttobebroken'

@app.before_request
def load_users():
    if 'user' in session:
        g.user = session['user']
       
    else:
        g.user = None


@app.route('/')
@app.route('/admlogin', methods=['GET', 'POST'])
def admlogin():

    if request.method == 'POST':
        uname = request.form['username'] 
        passd = request.form['password']
        user1 = Admin.query.filter_by(Username = uname).first()
        pass1 = Admin.query.filter_by(Password = passd).first()
        if user1 and  pass1:
            session['user'] = uname
            return redirect('/dash')
        else:
            flash("Invalid Credentials")

    return render_template('admlogin.html')

# @app.route('/navigation',methods=['GET','POST'])
# def navigate():
#     c=Admin.query.filter_by(Username = g.user).first()
#     admin1=c

#     return render_template('dash.html',admin1=admin1)




@app.route('/register',methods=['GET', 'POST'])
def register():
    msg = ''
    if (request.method == 'POST') :

        fristname1 = request.form['firstname'] 
        lastname1 = request.form['lastname'] 
        email1 = request.form['email']
        Ph_no1 = request.form['phone']
        pro1 = request.form['Pro'] 
        username1 = request.form['uname'] 
        password1 = request.form['password'] 
   
        email = Hdpuser.query.filter_by(Email = email1).first()
        phoneumber = Hdpuser.query.filter_by(Ph_no = Ph_no1).first()
        uname = Hdpuser.query.filter_by(Username = username1).first()
        if email:
            flash('Email address already exists')
        elif phoneumber:
            flash('Phone number already exists')
        elif uname:
            flash('Username already taken')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email1): 
            flash('Invalid email address input !')  
        elif not re.match(r'[789]\d{9}$', Ph_no1): 
            flash('Invalid phone number input !')
        else:
            entry = Hdpuser(FirstName=fristname1,  LastName =lastname1, Email =email1  , Ph_no=Ph_no1,Profession = pro1 , Username = username1,Password = password1  )
            db.session.add(entry)
            db.session.commit()
            flash("Added Succesfully")
    return render_template('patregis.html') 

@app.route('/doctorlogin', methods=['GET', 'POST'])
def doclogin():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username'] 
        passd = request.form['password']
        user1 = Doclogs.query.filter_by(Username = uname).first()
        pass1 = user1.Password
        if user1 and  passd==pass1:
            session['user'] = uname
            return render_template('docindex.html', user1 = user1)
        else:
            msg = "Wrong Credentials !"
    
    return render_template('doclogin.html',msg=msg)
    
       
@app.route('/dash')
def dash():
    
    d = Dataset.query.all()
    co = Hdpuser.query.all()
    co1 = Doclogs.query.all()
    co2 = Dataset.query.all()
    count = 0
    count1 = 0
    count2 = 0
    for i in co:
        count= count+1
    for i in co1:
        count1= count1+1
    for i in co2:
        count2= count2+1
    c22 = count2//2
    return render_template('dash.html',d = d,count=count,count1=count1,count2=count2,c22=c22)
 

@app.route('/patientlogin', methods=['GET', 'POST'])
def patlog():
     msg = ""
     if request.method == 'POST':
        uname = request.form['username'] 
        passd = request.form['password']
        user1 = Hdpuser.query.filter_by(Username = uname).first()
        pass1 = user1.Password
        if user1 and  passd==pass1:
            session['user'] = uname
           
            return render_template('profilepatient.html',user1=user1)
            
        else:
            msg = "Wrong Credentials !"
     return render_template('patlogin.html',msg = msg)


# @app.route('/form_elements')
# def form_elements():
#     return render_template('form_elements.html')



 
@app.route('/docregis',methods=['GET', 'POST'])
def docregis():
    msg = ''
    if (request.method == 'POST') :

        fristname2 = request.form['firstname'] 
        lastname2 = request.form['lastname'] 
        email2 = request.form['email']
        Ph_no2 = request.form['phone']
        pro2 = request.form['Pro'] 
        username2 = request.form['uname'] 
        password2 = request.form['password'] 
   
        email = Doclogs.query.filter_by(Email = email2).first()
        phoneumber = Doclogs.query.filter_by(Ph = Ph_no2).first()
        uname = Doclogs.query.filter_by(Username = username2).first()
        if email:
            flash('Email address already exists')
        elif phoneumber:
            flash('Phone number already exists')
        elif uname:
            flash('Username already taken')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email2): 
            flash('Invalid email address input !')  
        elif not re.match(r'[789]\d{9}$', Ph_no2): 
            flash('Invalid phone number input !')
        else:
            entry = Doclogs(Firstname=fristname2,  Lastname =lastname2, Email =email2  , Ph=Ph_no2,Profession = pro2 , Username = username2,Password = password2  )
            db.session.add(entry)
            db.session.commit()
            flash("Added Sucessfully")
    return render_template('docregis.html') 


@app.route('/pattable', methods=['GET', 'POST'])
def adminview():
    c = Hdpuser.query.all()
    return render_template('pattable.html',c = c)

@app.route('/doctable', methods=['GET', 'POST'])
def adminvdoc():
    c = Doclogs.query.all()
    return render_template('doctable.html',c = c)


@app.route('/emailcount',methods=['GET'])
def emailcount():
    c = Emails.query.all() 
    print(c) 
   
    return render_template('emailscount.html',c = c)

@app.route('/heartcheck',methods=['GET', 'POST'])
def heartcheck():
    return render_template("heartcheck.html")
        
     

        

@app.route('/predict',methods=['POST'])
def predict():  
    
    if request.method == 'POST':
   

        model = pickle.load(open('D:\keval\study\Projects\hdp\Heart_Disease_Prediction-FLask-\modal2.pkl','rb'))
       
        int_features = [ int(x) for x in request.form.values()]
         
        final_features=[np.array(int_features)]
        
        print(final_features)

        prediction=model.predict(final_features)
        
        output=round(prediction[0],2)
        if output == 1:
            o = "Bad News ! \n Their is a chance that you have a heart disease "
            return render_template('heartcheck.html',prediction_text='Heart status:  {}'.format(o))
        else:
            o =" Good News ! \n Their is a No chance that you have a heart disease ! :) "
            return render_template('heartcheck.html',prediction_text2='Heart status:  {}'.format(o))
        
     
    return redirect('/predict')

@app.route('/docpredict',methods=['POST'])
def docpredict():  
    
    if request.method == 'POST':

        model = pickle.load(open('D:\keval\study\Projects\hdp\Heart_Disease_Prediction-FLask-\modal2.pkl','rb'))
        
        int_features = [int(x) for x in request.form.values()]
        final_features=[np.array(int_features)]
        
        print(final_features)

        prediction=model.predict(final_features)
        
        output=round(prediction[0],2)
        if output == 1:
            o = "Bad News ! \n Their is a chance that you have a heart disease "
            return render_template('heartcheck.html',prediction_text='Heart status:  {}'.format(o))
        else:
            o =" Good News ! \n Their is a No chance that you have a heart disease ! :) "
            return render_template('heartcheck.html',prediction_text2='Heart status:  {}'.format(o))

    return redirect('/docpredict')
    
    


        # Age = request.form['age'] 
        # Sex = request.form['sex']
        # Cp = request.form['cp']
        # Trestbps = request.form['trestbps']
        # Cholestrol = request.form['cholestrol'] 
        # Fbs = request.form['Fbs'] 
        # Restecg = request.form['restecg'] 
        # Thalach = request.form['thalach'] 
        # Exang = request.form['exang'] 
        # Oldpeak = request.form['oldpeak'] 
        # Slope = request.form['slope'] 
        # Ca = request.form['ca'] 
        # Thal = request.form['thal'] 

        # return render_template('heartcheck.html', Age=Age, Sex=Sex, Cp=Cp  , Trestbps=Trestbps , Fbs=Fbs , Restecg=Restecg, Thalach=Thalach, Exang=Exang, Oldpeak=Oldpeak , Slope=Slope , Ca=Ca , Thal=Thal )

 #Down here All Are CRUD Opreations oF Database--------------------------------------------------------------------------------------------------------------------------------


#Admin view all data of user--------------------------------------------------------------------------------------------
@app.route('/pattable', methods=['GET', 'POST'])
def viewadmin():
    c = Hdpuser.query.all()
    return render_template("pattable.html",c = c)



#Admin view all data of Doctors--------------------------------------------------------------------------------------------
@app.route('/doctable', methods=['GET', 'POST'])
def vdocadmin():
    c = Doclogs.query.all()
    return render_template("doctable.html",c = c)


#Admin editing/updating all data of user-----------------------------------------------------------------------------------
@app.route('/adminup', methods=['GET', 'POST'])
def adminup():
     if request.method == 'POST':
        c = Hdpuser.query.get(request.form.get('id'))
        print(c)
        c.FirstName = request.form['name']
        c.LastName = request.form['name2']
        c.Email = request.form['email']
        c.Ph_no = request.form['phone']
        c.Username = request.form['usern']
        c.Password = request.form['pass']
        db.session.commit()
        flash("Patient detail Updated Successfully")
        return redirect("pattable")


#Admin editing/updating all data of Doctors------------------------------------------------------------------
@app.route('/admindocup', methods=['GET', 'POST'])
def admindocup():
     if request.method == 'POST':
        c = Doclogs.query.get(request.form.get('id'))
        
        c.Fristname = request.form['name']
        c.Lastname = request.form['name2']
        c.Ph = request.form['phone']
        c.Username = request.form['usern']
        c.Password = request.form['pass']
    
        db.session.commit()
        flash("Doctor Details Updated Successfully")
        return redirect("doctable")

#Admin Deleting  data of user------------------------------------------------------------------------
@app.route('/admindel/<id>/', methods = ['GET', 'POST'])
def admindel(id):
    c = Hdpuser.query.get(id)
    db.session.delete(c)
    db.session.commit()
    flash("Patient Deleted Successfully")
    return redirect('/pattable')

#Admin Deleting all data of Doctors-------------------------------------------------------------------
@app.route('/admindeldoc/<id>/', methods = ['GET', 'POST'])
def admindeldoc(id):
    c = Hdpuser.query.get(id)
    db.session.delete(c)
    db.session.commit()
    flash("Doc Deleted Successfully")
    return redirect('doctable')  
 
##Doctor-dashboard-related-code##---------------


@app.route('/viewdatatable')
def viewdatatable():
    ds = Dataset.query.all()
    c=Doclogs.query.filter_by(Username=g.user).first()

    print(c.Email)
    return render_template('datatable.html',ds=ds,c=c)


@app.route('/docindex')
def docindex():
   
    curr=Doclogs.query.filter_by(Username=g.user).first()

    print(curr.Email)
    
    return redirect('docindex')


@app.route('/viewpatient')
def viewpatient():
    patient=Hdpuser.query.all()
    c= Doclogs.query.filter_by(Username=g.user).first()

    return render_template('viewpatient.html',patient=patient,c=c)

@app.route('/userprofile')
def userprofile():
    c= Doclogs.query.filter_by(Username=g.user).first()
    return render_template('userprofile.html',c=c)

@app.route('/docupdate', methods=['GET', 'POST'])
def docupdate():
     if request.method == 'POST':
        d= Doclogs.query.filter_by(Username=g.user).first()
       
        d.Firstname = request.form['name1']
        d.Lastname = request.form['name2']
        d.Email = request.form['email']
        d.Ph = request.form['phone']
        d.Profession = request.form['pro']
        
        db.session.commit()
        flash("Doctor Details Updated Successfully")
        return redirect("userprofile")

@app.route('/profilepat')
def profilepat():
    c= Hdpuser.query.filter_by(Username=g.user).first()
    
    return render_template('profilepatient.html',c = c)

@app.route('/checkheart', methods=['GET', 'POST'])
def checkheart():
    return render_template('checkheart.html')

# payment module  ----------------------------------------------------------------------------------------------------------
@app.route('/payment', methods=['GET', 'POST'])
def payhome():
    return render_template('paymenthome.html')

@app.route('/success')
def success():
    return render_template('paysucces.html')

@app.route('/pay',methods=['POST','GET'])
def pay():
    if request.method == 'POST':
        name = request.form.get('name')
        purpose = request.form.get('purpose')
        email = request.form.get('email')
        amount = request.form.get('amount')
        
        response = api.payment_request_create(
        amount=amount,
        purpose=purpose,
        buyer_name=name,
        send_email=True,
        email=email,
        redirect_url="http://localhost:5000/success"
        )
        
        return redirect(response['payment_request']['longurl'])
    
    else:
        
        return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)