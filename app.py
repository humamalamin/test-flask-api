from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from urllib import request as reqUrlLib
from urllib.request import Request, urlopen
import json
from sqlalchemy import create_engine,insert,MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1:3306/test_flask'
db = SQLAlchemy(app)
ma = Marshmallow(app)

metadata = MetaData()
# Base = declarative_base()
# MODELS
class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    avatar = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    avatar = ma.auto_field()

@app.route('/')
def root():
    return 'api runing'

ROWS_PER_PAGE=10

@app.route('/user', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.json
        query = insert(User).values(email=data.get("email"),first_name=data.get("first_name"),last_name=data.get("last_name"),avatar=data.get("avatar"))
        db.session.execute(query)
        db.session.commit()
        return jsonify({"message":"success"}),201
    else:
        page = request.args.get('page', 1, type=int)
        get_users = User.query.paginate(page=page,per_page=ROWS_PER_PAGE)
        user_schema = UserSchema(many=True)
        users = user_schema.dump(get_users)

        result = {
            "page": page,
            "per_page": ROWS_PER_PAGE,
            "total": get_users.total,
            "total_pages": get_users.pages,
            "data": users
        }

        return jsonify(result)

@app.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
def user(id):
    if request.method == 'GET':
        get_user = User.query.get(id)
        user_schema = UserSchema(many=False)
        user = user_schema.dump(get_user)
        
        return jsonify(user)
    elif request.method == 'PUT':
        user = User.query.get(id)
        data = request.json
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        avatar = data.get('avatar')

        user.email = email
        user.last_name = last_name
        user.first_name = first_name
        user.avatar = avatar

        db.session.commit()
        user_schema = UserSchema(many=False)
        users = user_schema.dump(user)
        return jsonify(users)
    else:
        header = request.headers.get("Authorization")
        if header != "3cdcnTiBsl":
            return jsonify({"message": "Unauthorized"}),401
        else:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()

            return jsonify({"message":"success"})

@app.route('/user/fetch')
def get_user():
    url = "https://reqres.in/api/users?page=1"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(request).read()
    dict = json.loads(response)

    query = insert(User)
    values_list = dict["data"]

    db.session.execute(query,values_list)
    db.session.commit()

    return jsonify(dict["data"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)