from flask import Flask, render_template, request, redirect
import csv
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv(override=True)

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


# @app.route('/index.html')
# def my_home_index():
#     return render_template('index.html')
#
# @app.route('/works.html')
# def my_works():
#     return render_template('works.html')
#
# @app.route('/about.html')
# def my_about():
#     return render_template('about.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_data_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email}, {subject}, {message}')




def send_whatsapp(email, message):
    account_sid = 'ACa1a497c8a2b31b3322a0f61422f8e6b0'
    SECRET_KEY = os.getenv("SECRET_KEY")
    auth_token = SECRET_KEY
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'{email} sent you: {message}',
        to='whatsapp:+59898394287'
    )


def write_data_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])
        send_whatsapp(email, message)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_data_to_csv(data)
            return redirect('thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong, try again.'

# @app.route('/about/<username>/<int:post_id>')
# def about(username=None, post_id=None):
#     return render_template('about.html', name=username, post_id=post_id)
