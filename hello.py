from flask import Flask, request, render_template
import redis
import urllib
#import operator
import pypandoc
#import re

redis = redis.StrictRedis(
    host='pub-redis-10073.us-east-1-3.3.ec2.garantiadata.com',
    port='10073', db=0)
app = Flask(__name__)

class Tag():
    def __init__(self, name, onMER):
        self.name = name
        self.onMER = onMER
        
    def __str__(self):
        return self.name

        
def read_tags():
    raw = urllib.urlopen("http://wiki.ubc.ca/Science:MER/Lists/Popular_tags").read()
    raw_split = raw.split('MER Tag ')
    list_tags = []
    for chunk in raw_split:
        tag = chunk.split('"')[0]
        if not "<" in tag:
            list_tags.append(tag)
    return sorted(list_tags)

def url_from_info(course, exam, question):
    return ("http://wiki.ubc.ca/Science:Math_Exam_Resources/Courses/" + course + "/" + exam + "/" + question)

def hint_from_question_url(base):
    hint_url = base.replace('Science:', 'index.php?title=Science:') + '/Hint_1&action=raw'
    hint_raw = urllib.urlopen(hint_url).read().decode('utf-8')
    hint_raw = hint_raw.replace('\n', '').replace('<math>', '$').replace('</math>', '$').replace('$begin{align}', '\n $begin{align}').replace('end{align}$', 'end{align}$ \n\n')
    hint = pypandoc.convert(hint_raw, 'latex', format='html')
    return hint_raw

def solution_from_question_url(base):
    sol_url = base.replace('Science:', 'index.php?title=Science:') + '/Solution_1&action=raw'
    sol_raw = urllib.urlopen(sol_url).read().decode('utf-8')
    sol_raw = sol_raw.replace('\n', '').replace('<math>', '$').replace('</math>', '$').replace('$begin{align}', '\n $begin{align}').replace('end{align}$', 'end{align}$ \n\n')
    sol = pypandoc.convert(sol_raw, 'latex', format='html')
    return sol_raw

@app.route('/<course>/<exam>/<question>')
def show_existing(course, exam, question):
    question_url = url_from_info(course, exam, question)
    hint = hint_from_question_url(question_url)
    solution = solution_from_question_url(question_url)
    return render_template("communicate.html", myhint=hint, mysol=solution)

@app.route('/')
def hello():
#    to_store = read_tags()
#    to_store.append('test tag not on MER')
#    redis.delete('allTags')
#    for tag in to_store:
#        redis.rpush('allTags', tag)
    hint = redis.get('hint').decode('utf-8')
    sol = redis.get('sol').decode('utf-8')
    stored_tags = redis.lrange('allTags', 0, -1)
    MER_tags = read_tags()
    not_on_MER = [item for item in stored_tags if item not in MER_tags]
    return render_template("communicate.html",
                           myhint=hint, mysol=sol, tags=MER_tags, tags_not_on_MER=not_on_MER)


@app.route('/', methods=['POST'])
def communicate_post():
    if request.form['submit'] == 'preview':
        hint = request.form['inputHint']
        sol = request.form['inputSol']
        stored_tags = redis.lrange('allTags', 0, -1)
        MER_tags = read_tags()
        not_on_MER = [item for item in stored_tags if item not in MER_tags]
        return render_template("communicate.html",
                               myhint=hint, mysol=sol, tags=MER_tags, tags_not_on_MER=not_on_MER)
    
    elif request.form['submit'] == 'submit':
        hint = request.form['inputHint']
        sol = request.form['inputSol']
        redis.set('hint', hint)
        redis.set('sol', sol)
        stored_tags = redis.lrange('allTags', 0, -1)
        MER_tags = read_tags()
        not_on_MER = [item for item in stored_tags if item not in MER_tags]
        return render_template("communicate.html",
                               myhint=hint, mysol=sol, tags=MER_tags, tags_not_on_MER=not_on_MER)
    else:
        return "Something went wrong"

if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
