from flask import Flask, render_template, session, request, redirect 
import random 

app = Flask(__name__)
app.secret_key = 'thisIsSecret'

@app.route('/')
def index():
	session['number'] = random.randrange(0,100)
	print (session['number'])
	return render_template("index.html")

@app.route('/guess', methods=['POST'])
def result():
	guess = int(request.form['guess'])
	if guess == session['number']:
	    answer = "Correct"
	    return render_template("index.html", answer=answer)
	elif guess < session['number']:
	    answer = "Too Low"
	    return render_template("index.html", answer=answer)
	else:
	    answer = "Too High"
	    return render_template("index.html", answer=answer)

app.run(debug=True)