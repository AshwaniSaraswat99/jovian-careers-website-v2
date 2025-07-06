from flask import Flask,render_template,jsonify,request,redirect,session, flash
from database import load_jobs_from_db,load_job_from_db,add_application_to_db,check_user_credentials,check_user_exists,create_new_user
from typing import Optional, Dict, Any
from datetime import timedelta
import os


app = Flask(__name__)
app.secret_key = os.environ.get('Secret_Key')
# JOBS = [
#     {
#         "id": 1,
#         "title": "Data Analyst",
#         "location": "Bengaluru, India",
#         "salary": "Rs. 10,00,000"
#     },
#     {
#         "id": 2,
#         "title": "Data Scientist",
#         "location": "Delhi, India",
#         "salary": "Rs. 15,00,000"
#     },
#     {
#         "id": 3,
#         "title": "Frontend Engineer",
#         "location": "Remote",
#         "salary": "Rs. 12,00,000"
#     },
#     {
#         "id": 4,
#         "title": "Backend Engineer",
#         "location": "San Francisco, USA",
#         "salary": "$120,000"
#     }
# ]

@app.route('/')
def hello_world():
    print("hello")
    jobs=load_jobs_from_db()
    
    return render_template('home.html',jobs=jobs,company_name="Jovian")
@app.route('/job/<id>')
def show_job(id):
    job=load_job_from_db(id)
    if not job:
        return "Not Found",404
    return render_template('jobpage.html',job=job)
    

@app.route('/api/jobs')
def list_jobs():
    jobs=load_jobs_from_db()
    return jsonify(jobs)

@app.route('/job/<id>/apply', methods=['POST'])
def apply(id):
    data = request.form
    job = load_job_from_db(id)
    add_application_to_db(id, data)
    return render_template('application_submitted.html', application=data, job=job)

@app.route("/login", methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        raw_user=check_user_credentials(username ,password,'user')
        user: Optional[Dict[str, Any]] = dict(raw_user) if raw_user else None
        if user:
            session['user_id']=user['id']

            if remember == 'on':
                app.permanent_session_lifetime = timedelta(days=30)
                session.permanent = True
            else:
                session.permanent=False
            return redirect('/')
        return "Invalid credentials",401     
    return render_template('login_user.html',)

@app.route("/logout", methods=['GET','POST'])
def logout_user():
    session.clear()
    return redirect('/')

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        captcha = request.form.get('captcha')
        expected_captcha = session.get('captcha_value')

        # 1. Check if user already exists
        if check_user_exists(email=email, username=username):
            flash("User already exists. Please login instead.", "warning")
            return redirect('/login')

        # 2. Check password match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect('/sign_up')

        # 3. Validate CAPTCHA
        if captcha != expected_captcha:
            flash("Invalid CAPTCHA. Please try again.", "danger")
            return redirect('/sign_up')

        # 4. Create new user
        try:
            create_new_user(email, username, phone, password, confirm_password)
            flash("Sign-up successful! Please log in.", "success")
            return redirect('/login')
        except Exception as e:
            print("Error creating user:", e)
            flash("Something went wrong. Please try again.", "danger")
            return redirect('/sign_up')

    # GET request → show the signup form
    return render_template('signup.html')



if __name__=='__main__':
    app.run( host='0.0.0.0',debug=True)