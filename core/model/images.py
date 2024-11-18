from core import db
from datetime import datetime
from core.libs.assertions import assert_valid,assert_found
from core.model.user import User
from core.apis.common import save_image

class CarImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.String(80), db.ForeignKey(User.id, name='fk_images_user_id'), nullable=False)
    date = db.Column(db.TIMESTAMP(timezone=True), default= datetime.utcnow, nullable=False)

    img1 = db.Column(db.String(500),nullable=True)
    img2 = db.Column(db.String(500),nullable=True)
    img3 = db.Column(db.String(500),nullable=True)
    img4 = db.Column(db.String(500),nullable=True)
    img5 = db.Column(db.String(500),nullable=True)
    img6 = db.Column(db.String(500),nullable=True)
    img7 = db.Column(db.String(500),nullable=True)
    img8 = db.Column(db.String(500),nullable=True)
    img9 = db.Column(db.String(500),nullable=True)
    img10 = db.Column(db.String(500),nullable=True)


    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)
    
    @classmethod
    def add(cls, data):
        rawimages = data['images']
        images=[]
        for image in rawimages:
            images.append(save_image(image))
        image_fields = {}
        for i in range(1, 11):
            image_fields[f'img{i}'] = images[i - 1] if i <= len(images) else None

        # Create a CarImages instance with dynamic fields and user_id
        car_image_instance = cls(user_id=data['user_id'], **image_fields)

        # Add to session and commit
        db.session.add(car_image_instance)
        db.session.flush()
        return car_image_instance.id

    @classmethod
    def Delete(cls, data):
        url_object = cls.filter(cls.id==data['url_id'],cls.user_id==data['user_id']).first()
        assert_found(url_object, "images not found")
        db.session.delete(url_object)
        db.session.flush()

    @classmethod
    def VeiwCarUrls(cls, data):
        images = cls.filter(cls.id==data['url_id'],cls.user_id==data['user_id']).first()
        assert_found(images, "veiw unavalable")
        return images
    
    @classmethod
    def Update(cls,data):
        if('deleted' in data):
            for x in data['deleted']:
                temp = cls.filter(cls.id==data['url_id']).first()
                if temp:
                    setattr(temp, f'img{x}', None)
                db.session.flush()