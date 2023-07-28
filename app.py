
from flask import Flask,request,render_template,redirect,url_for
from database import verifyLogin,verifyAccountCreation
import forms
app=Flask(__name__)
app.run(debug=True)
app.config['SECRET_KEY']='RVCE'
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/login",methods=["POST","GET"])
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
       
        email=form.email.data
        password=form.password.data
        if(verifyLogin(email,password)):
            return redirect(url_for("mainPage"))
        return render_template("login.html",errorMsg="Invalid email id or password",form=form)
        
    return render_template("login.html",form=form)


@app.route("/signUp",methods=["GET","POST"])
def signUp():

    form=forms.SignUpForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        confirmPassword=form.confirmPassword.data
       
        errorMessage=verifyAccountCreation(email,password,confirmPassword)
       
        if(errorMessage):
            return render_template("signUp.html",form=form,errorMessage=errorMessage)
        return redirect(url_for("mainPage"))
    
    return render_template("signUp.html",form=form)
   
@app.route("/mainPage")
def mainPage():
    return render_template("main.html")

 


if __name__ == '__main__':
    app.run(debug=True)
