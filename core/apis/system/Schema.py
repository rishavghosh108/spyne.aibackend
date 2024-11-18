from marshmallow import Schema, fields, validates_schema, ValidationError

def validate_integer_length(n):
    def validator(value):
        if len(str(value))!=n:
            raise ValidationError(f'The integer must have exactly {n} digits.')
    return validator

class UserDataSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
        

class LoginForgetSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class ProfileSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)