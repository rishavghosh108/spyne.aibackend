from marshmallow import Schema, fields, validates_schema, ValidationError, validates,validate
from werkzeug.datastructures import FileStorage

class CarSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    tags = fields.String(required=True)
    images = fields.List(
        fields.Raw(),
        validate=lambda files: 0 <= len(files) <= 10,
        required=True,
        error_messages={"required": "Images field is required."}
    )

    @validates('images')
    def validate_images(self, value):
        if not isinstance(value, list):
            raise ValidationError("Images must be provided as a list.")

        for file in value:
            if not isinstance(file, FileStorage):
                raise ValidationError("Each item in images must be a valid file.")
            if not file.mimetype.startswith("image/"):
                raise ValidationError(f"Invalid file type for {file.filename}. Only images are allowed.")
            if file.content_length > 10 * 1024 * 1024:
                raise ValidationError(f"File {file.filename} exceeds the maximum allowed size of 10 MB.")

class CarsSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    url_id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    tags = fields.String(required=True)

class CarDeleteSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    url_id = fields.Integer(required=True)

class VeiwCarSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    url_id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    tags = fields.String(required=True)
    images = fields.List(fields.String(), validate=validate.Length(min=0, max=10), required=False, allow_none=True)

class UpdateCarSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    url_id = fields.Integer(required=True)

    title = fields.String(required=False)
    description = fields.String(required=False)
    tags = fields.String(required=False)
    deleted = fields.List(fields.Integer(), validate=validate.Length(min=0, max=10), required=False)

    @validates_schema
    def validate_fields(self, data, **kwargs):
        if not (data.get('title') or data.get('description') or data.get('tags') or data.get('deleted').length>0):
            raise ValidationError('At least one of title, description, tags or images must be provided.')

