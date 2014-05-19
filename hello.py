from flask import Flask, request, render_template
#from redis import Redis as redis

app = Flask(__name__)


@app.route('/')
def hello():
#    name = redis.get('name').decode('utf-8')
    return render_template("communicate.html", myhint='', mysol='')


@app.route('/', methods=['POST'])
def communicate_post():
    if request.form['submit'] == 'submit':
        hint = request.form['inputHint']
        sol = request.form['inputSol']
        return render_template("communicate.html", myhint=hint, mysol=sol)
    else:
        return "Something went wrong"

if __name__ == "__main__":
	app.run()
