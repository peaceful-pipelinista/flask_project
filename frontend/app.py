import os
from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests

BACKEND_URL = os.getenv("BACKEND_URL")

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

@app.route('/signup')
def signup():
    now = datetime.now()
    return render_template(
        'signup.html',
        date=now.strftime("%d-%m-%Y"),
        day=now.strftime("%A"),
        time=now.strftime("%H:%M:%S")
    )

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)

    # requests.post(
    #     f"{BACKEND_URL}/add",
    #     json=form_data
    # )

    # return redirect('/success')

    try:
        response = requests.post(
            f"{BACKEND_URL}/add",
            json=form_data,
            timeout=5
        )

        if response.status_code == 201:
            return redirect('/success')
        else:
            raise Exception("Failed to submit data")

    except Exception as e:
        now = datetime.now()
        return render_template(
            'signup.html',
            error=str(e),
            date=now.strftime("%d-%m-%Y"),
            day=now.strftime("%A"),
            time=now.strftime("%H:%M:%S")
        )

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/view')
def view():
    response = requests.get(f"{BACKEND_URL}/view")
    users = response.json()
    return render_template('view.html', users=users)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
