from flask import Flask, request, render_template
import redis

redis = redis.StrictRedis(host = 'pub-redis-10073.us-east-1-3.3.ec2.garantiadata.com' , port = '10073' , db = 0)
app = Flask(__name__)


@app.route('/')
def hello():
#    name = redis.get('name').decode('utf-8')
    hint = redis.get('hint').decode('utf-8')
    sol = redis.get('sol').decode('utf-8')
    both = hint + sol
    return render_template("communicate.html", myhint='', mysol='', both=both)


@app.route('/', methods=['POST'])
def communicate_post():
    if request.form['submit'] == 'preview':
        hint = request.form['inputHint']
        sol = request.form['inputSol']
        redis.set('hint', hint)
        redis.set('sol', sol)
        both = hint + sol
        return render_template("communicate.html", myhint=hint, mysol=sol, both = both)
    else:
        return "Something went wrong"

if __name__ == "__main__":
	app.run(debug=True)
