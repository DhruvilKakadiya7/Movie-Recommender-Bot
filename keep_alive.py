from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def keep_alive():
  if __name__ == "__main__":
    app.run(debug=True)
