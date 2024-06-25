from flask_app import socketio,app
from flask_app.controllers import users,houses,messages



if __name__=="__main__":
    socketio.run(app, debug=True)