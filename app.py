from flask import Flask,render_template,jsonify,request,redirect,session
from database import load_jobs_from_db,load_job_from_db,add_application_to_db,check_user_credentials
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
        


if __name__=='__main__':
    app.run( host='0.0.0.0',debug=True)