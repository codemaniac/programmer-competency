
import random
import string
import simplejson as json
import sqlite3 as db
from flask import Flask, request, render_template

app = Flask(__name__)

def _save(key, choices):
  con = db.connect('../db/store.db')
  with con:  
    cur = con.cursor()
    query = '''INSERT INTO competencies VALUES("%s", "%s")''' % (key, choices)
    cur.execute(query)

def _retreive(key):
  con = db.connect('../db/store.db')
  con.text_factory = str
  with con:  
    cur = con.cursor()
    query = '''SELECT competency FROM competencies WHERE key="%s"''' % key
    cur.execute(query)
    row = cur.fetchone()       
    return row[0]

@app.route('/api/submit', methods = ['POST'])
def submit():
  choices = request.json['choices']
  key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(8))
  _save(key, choices)
  return json.dumps({'key' : key})

@app.route('/<key>')
def review(key):
  choices = _retreive(key).encode('utf8')
  choices = choices.replace('u\'', '').replace('\'', '').replace('{', '').replace('}', '')
  choices_list = []
  for c in choices.split(','):
    c = c.split(':')[1].strip()
    choices_list.append(c)
  return render_template('index.html', retreival=True, choices=choices_list)

@app.route('/')
def index():
  return render_template('index.html', retreival=False)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
