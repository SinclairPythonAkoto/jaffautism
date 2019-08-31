from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import requests

app = Flask(__name__)

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
		from clockwork import clockwork
		api = clockwork.API('923a9a3d3f680a9ae95a5198afd6b1eadb428be1',)

		message = clockwork.SMS(
		    to = '447481790498',
		    message = f'{txt}',
		    from_name=f'{sender}')

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
		if user == 'sandra' and userPassword == 'sandra':
			session['logged_in'] = True
			flash('You have just logged in!')
			return redirect(url_for('JonnyAdmin'))
		else:
			error = 'Invalid credentials. You can only log in if you are part of management of Jonny & Friends 4 Autism.'
	return render_template('login.html', error=error, title=title)


@app.route('/JonnyAdmin', methods=['GET', 'POST'])
@login_required
def JonnyAdmin():
	if request.method == 'GET':
		return render_template('JonnyAdmin.html')
	else:
		num = request.form.get('number')
		txt = request.form.get('sendText')
		from clockwork import clockwork
		api = clockwork.API('923a9a3d3f680a9ae95a5198afd6b1eadb428be1',)

		message = clockwork.SMS(
		    to = f'{num}',
		    message = f'{txt}',
		    from_name='MrAkotoApps')

		response = api.send(message)

		if not response.success:
			return render_template('JonnyAdmin.html', num=num, txt=txt)
		else:
			flash('message failed to send.')
			return redirect(url_for('JonnyAdmin'))


@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('See you soon!')
	return redirect(url_for('textJonny'))


if __name__ == '__main__':
    app.run(debug=True)