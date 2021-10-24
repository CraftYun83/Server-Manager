from flask import Flask, request
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return 'Hello. I am alive! <br> <a href="/logs">Click here to see bot logs</a>'

@app.route('/logs')
def logs():
  f = open("log.txt", "r")
  return f.read().replace("\n", "<br>")

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()