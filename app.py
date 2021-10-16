from website import app
import os
from selenium import webdriver

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", threaded=True, port=int(os.environ.get('PORT', 33507))) #do heroku