from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

CREDENTIALS_FILE = '.credentiels.txt'
RESULTS_FILE = '.results.txt'

# Utility function to read credentials
def read_credentials():
    with open(CREDENTIALS_FILE, 'r') as f:
        return [line.strip().split(',') for line in f]

# Utility function to write credentials
def write_credentials(credentials):
    with open(CREDENTIALS_FILE, 'w') as f:
        for credential in credentials:
            f.write(','.join(credential) + '\n')

# Utility function to read results
def read_results():
    with open(RESULTS_FILE, 'r') as f:
        return {line.split(',')[0]: int(line.split(',')[1]) for line in f}

# Utility function to write results
def write_results(results):
    with open(RESULTS_FILE, 'w') as f:
        for choice, count in results.items():
            f.write(f"{choice},{count}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        credentials = read_credentials()

        for credential in credentials:
            if credential[0] == email and credential[1] == password and credential[2] == '0':
                # Successful login, redirect to vote page
                return redirect(url_for('vote', email=email))
        flash('Invalid credentials or account already used for voting.')
    return render_template('login.html')

@app.route('/vote/<email>', methods=['GET', 'POST'])
def vote(email):
    if request.method == 'POST':
        choice = request.form['choice']
        results = read_results()
        results[choice] += 1
        write_results(results)

        # Update user's voting status
        credentials = read_credentials()
        for credential in credentials:
            if credential[0] == email:
                credential[2] = '1'
                break
        write_credentials(credentials)

        flash('Vote submitted successfully!')
        return redirect(url_for('login'))

    return render_template('vote.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle form submission (e.g., send email, save to database, etc.)
        flash('Thank you for contacting us!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    # Initialize results file if not exists
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w') as f:
            f.write("Choice1,0\nChoice2,0\nChoice3,0\n")

    app.run(debug=True)
