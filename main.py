from website import app
import os

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", threaded=True, port=int(os.environ.get('PORT', 33507))) #do heroku