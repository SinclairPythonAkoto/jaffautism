from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import requests
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '****', # jonny email
    MAIL_PASSWORD = '****', # email password
    MAIL_DEFAULT_SENDER = ('Jonny & Friends For Autism', 'jonnyandfriends4autism.@gmail.com'), #('NAME OR TITLE OF SENDER', 'SENDER EMAIL ADDRESS')
    MAIL_MAX_EMAILS = 5
))

mail = Mail(app)


# need to set secret key for login_required function to work
app.secret_key = "Shalieka"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to sign in first')
			return redirect(url_for('login'))
	return wrap

@app.route('/', methods=['GET', 'POST'])
# @login_required
def textJonny():
	if request.method == 'GET':
		return render_template('textJonny.html')
	else:
		txt = request.form.get('sendText')
		sender = request.form.get('senderName')
		num = request.form.get('contactNumber')
		from clockwork import clockwork
		api = clockwork.API('****',) # api key

		message = clockwork.SMS(
		    to = '****', # number text is being sent to 
		    message = f'FROM: {sender.lower()}\nNUMBER: {num}\n\n{txt.lower()}',
		    from_name='jaffautism')

		response = api.send(message)

		if response.success:
			return render_template('textJonny.html', txt=txt, sender=sender)
		else:
			return redirect(url_for('textJonny'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	title = "Jaffa Login"
	error = None
	if request.method == 'GET':
		return render_template('login.html')
	else:
		user = request.form.get("username")
		userPassword = request.form.get("password")
		if user == '****' and userPassword == '****':
			session['logged_in'] = True
			flash('You have just logged in!')
			return redirect(url_for('JonnyAdmin'))
		else:
			error = 'Invalid credentials. You can only log in if you are part of management of Jonny & Friends 4 Autism.'
	return render_template('login.html', error=error, title=title)


@app.route('/JonnyAdmin', methods=['GET', 'POST'])
@login_required
def JonnyAdmin():
	title = "JAFFA Admin!"
	if request.method == 'GET':
		return render_template('JonnyAdmin.html', title=title)
	else:
		num = request.form.get('number')
		txt = request.form.get('sendText')
		from clockwork import clockwork
		api = clockwork.API('****',) # api key

		message = clockwork.SMS(
		    to = f'{num}',
		    message = f'{txt.lower()}',
		    from_name='jaffautism')

		response = api.send(message)

		if not response.success:
			return render_template('JonnyAdmin.html', num=num, txt=txt)
		else:
			flash('message failed to send.')
			return redirect(url_for('JonnyAdmin'))


@app.route('/send_mail', methods=['GET', 'POST'])
@login_required
def send_mail():
	if request.method == 'GET':
		return render_template('send_mail.html')
	else:
		sendTo = request.form.get('emailReciever')
		confirmEmail = request.form.get('confirm')
		content = request.form.get('emailContent')
		sub = request.form.get('emailSubject')


		msg = Message(f'{sub}', recipients=[sendTo])
		msg.body = f'{content}\nKind regards\n\nSandra Ferguson\nJonny And Friends For Autism'

		with app.open_resource('logo1.png') as logo:
			msg.attach('logo1.png', 'image/png', logo.read())

		mail.send(msg)
		return redirect(url_for('JonnyAdmin'))
	

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('See you soon!')
	return redirect(url_for('textJonny'))


if __name__ == '__main__':
    app.run(debug=True)