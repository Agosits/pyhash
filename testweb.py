from flask import Flask
import logging
app = Flask(__name__)

@app.route('/')
def index():
    print 'log'
    logging.error('this is log')
    return 'hee'

if __name__ == '__main__':
    print 'testweb'
    app.run()
