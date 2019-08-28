from flask import Flask, jsonify, request
#from flask_cors import CORS, cross_origin
import app.database.UserModel as UserModel

app = Flask(__name__, static_url_path='/static')

#CORS(app)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/getTableHeader')
def getTableHeader():
    column = UserModel.getColumn()
    return jsonify({'header': column})


#----------- CRUD --------------#
@app.route('/getUserList/', defaults={'page': 1})
@app.route('/getUserList/<page>', defaults={'page': 1})
def getUserList(page):
    if not page or page < 1:
        page = 1
    data = UserModel.getUserList(page)
    if(data):
        return jsonify({'data': data})
    else:
        return jsonify({'error': data})


#@cross_origin(origin='*')
@app.route('/searchUser', methods=['POST'])
def searchUser():
    data = request.json
    result = UserModel.searchUserList(data['whereMap'])
    #print(data['whereMap'])
    if result :
        return jsonify({'data': result})
    else:
        return jsonify({'error': data})


#@cross_origin(origin='*')
@app.route('/createUser', methods=['POST'])
def createUser():
    data = request.json
    return str(UserModel.createUser(data))


#@cross_origin(origin='*')
@app.route('/editUser', methods=['POST'])
def editUser():
    data = request.json
    return str(UserModel.editUser(data))


#@cross_origin(origin='*')
@app.route('/delUser', methods=['POST'])
def delUser():
    data = request.json
    if data['id']:
        return str(UserModel.delUser(data))
    else:
        return False
