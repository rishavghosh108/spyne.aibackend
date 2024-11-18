from core import db
from datetime import datetime
from core.libs.assertions import assert_valid,assert_found
from werkzeug.security import check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password=db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    date = db.Column(db.TIMESTAMP(timezone=True), default= datetime.utcnow, nullable=False)

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)
    
    @classmethod
    def UserCheck(cls, data):
        user=cls.filter(cls.email==data['email']).first()
        assert_valid(user is None,"user already exist !!!")

    @classmethod
    def signup(cls,data):
        cls.UserCheck(data)
        user = cls(name=data['name'],email=data['email'],password=data['password'])
        db.session.add(user)
        db.session.flush()

    @classmethod
    def login(cls,data):
        user = cls.filter(cls.email==data['email']).first()
        assert_found(user,"user does not exist !!!")
        assert_valid(check_password_hash(user.password, data['password']),"incorrect password")
        return user.id
    
    @classmethod
    def profile(cls,user_id):
        user = cls.filter(cls.id==user_id).first()
        assert_found(user,"user does not exist !!!")
        return user

    # @classmethod
    # def forget(cls,data):
    #     user = cls.filter(cls.email==data['email'],cls.type==data['type']).first()
    #     assert_found(user,"user does not exist !!!")
    #     assert_valid(not check_password_hash(user.password, data['password']), "same as password !!!")

    # @classmethod
    # def change_password(cls,data):
    #     user=cls.filter(cls.email==data['email'],cls.type==data['type']).first()
    #     assert_found(user,"user does not exist !!!")
    #     user.password=data['password']
    #     db.session.flush()