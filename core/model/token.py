from core.model.user import User
from core import db
from datetime import datetime
import random,string
from core.libs.assertions import assert_valid,assert_found


class Token(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(12),nullable=False)
    date = db.Column(db.TIMESTAMP(timezone=True), default= datetime.utcnow, nullable=False)

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)
    
    @classmethod
    def create_token(cls,data):
        user = User.UserCheck(data)
        assert_valid(user is None,"user already exist !!!")
        check = cls.filter(cls.email==data['email']).first()
        assert_valid(check is None,"email already exist !!!")
        tokenString = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        token = cls(email=data['email'], token=tokenString)
        # send token to this email
        db.session.add(token)
        db.session.flush()

    @classmethod
    def check_token(cls,data):
        token = cls.filter(cls.email==data['email'], cls.token==data['token']).first()
        assert_found(token,"invalid credaintials !!!")
        return token