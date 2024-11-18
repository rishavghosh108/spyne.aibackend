from core import db
from datetime import datetime
from core.libs.assertions import assert_valid,assert_found
from core.model.images import CarImages
from core.model.user import User

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(80), db.ForeignKey(User.id, name='fk_car_user_id'), nullable=False)
    url_id = db.Column(db.String(80), db.ForeignKey(CarImages.id, name='fk_car_images_id'),nullable=False)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    date = db.Column(db.TIMESTAMP(timezone=True), default= datetime.utcnow, nullable=False)

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)
    
    @classmethod
    def add(cls,data):
        url = CarImages.add(data)
        car = cls(url_id=url, user_id=data['user_id'], title = data['title'],description = data['description'], tags = data['tags'])
        db.session.add(car)
        db.session.flush()

    @classmethod
    def GetAll(cls,user_id):
        return cls.filter(cls.user_id==user_id).all()
    
    @classmethod
    def Delete(cls,data):
        car_object = cls.filter(cls.id==data['id'],cls.user_id==data['user_id'],cls.url_id==data['url_id']).first()
        assert_found(car_object,'details not found')
        CarImages.Delete(data)
        db.session.delete(car_object)
        db.session.flush()

    @classmethod
    def VeiwCar(cls, data):
        car_object=db.session.query(Car, CarImages).join(CarImages, Car.url_id == CarImages.id).filter(
        Car.id == data['id'],
        Car.user_id == data['user_id'], 
        Car.url_id == data['url_id']
    ).first()
        assert_found(car_object,'details not found')
        car, car_images = car_object
        images = [getattr(car_images, f'img{i}') for i in range(1, 11) if getattr(car_images, f'img{i}')]

        return {
            "id": car.id,
            "user_id": car.user_id,
            "url_id": car.url_id,
            "title": car.title,
            "description": car.description,
            "tags": car.tags,
            "images": images
        }
    
    @classmethod
    def UpdateCarDetails(cls,data):
        car = cls.filter(cls.id==data['id'], cls.user_id==data['user_id'], cls.url_id==data['url_id']).first()
        assert_found(car, "car not found")
        if('title' in data):
            car.title=data['title']
        if('tags' in data):
            car.tags=data['tags']
        if('description' in data):
            car.description = data['description']

        CarImages.Update(data)

        db.session.flush()