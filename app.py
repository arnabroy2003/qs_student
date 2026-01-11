from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = 'aspro1111'

# Load all 6 CSVs
courses = {
    'python': pd.read_csv('python.csv'),
    'ai': pd.read_csv('ai.csv'),
    'frontend': pd.read_csv('frontend.csv'),
    'backend': pd.read_csv('backend.csv'),
    'webdev': pd.read_csv('basicweb.csv'),
    'c': pd.read_csv('c.csv')
}

@app.route('/')
def home():
    return render_template('login2.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email'].strip().lower()
    name = None

    # To store drive links
    drive_links = {
        'python_link': None,
        'aiml_link': None,
        'frontend_link': None,
        'backend_link': None,
        'webdev_link': None,
        'c_link': None
    }

    # Loop through each course and check if email exists
    for course, df in courses.items():
        user = df[df['email'].str.lower() == email]
        if not user.empty:
            if not name:
                name = user.iloc[0]['fullname']  # Get name from any matched course
            link = user.iloc[0]['Link']
            if course == 'python':
                drive_links['python_link'] = link
            elif course == 'ai':
                drive_links['aiml_link'] = link
            elif course == 'frontend':
                drive_links['frontend_link'] = link
            elif course == 'backend':
                drive_links['backend_link'] = link
            elif course == 'webdev':
                drive_links['webdev_link'] = link
            elif course == 'c':
                drive_links['c_link'] = link

    if name:  # if matched
        session['email'] = email
        session['name'] = name
        session.update(drive_links)
        return redirect(url_for('dashboard'))
    else:
        return render_template('login2.html', error="Invalid email")

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect('/')
    return render_template(
        'dash2.html',
        name=session['name'],
        frontend_link=session.get('frontend_link'),
        python_link=session.get('python_link'),
        backend_link=session.get('backend_link'),
        webdev_link=session.get('webdev_link'),
        c_link=session.get('c_link'),
        aiml_link=session.get('aiml_link')
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
