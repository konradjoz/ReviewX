from mongoengine import Document, IntField, StringField, EmailField, DateTimeField, BooleanField


class User(Document):
    # Defines collection name
    meta = {'collection': 'User'}

    user_id = IntField(required=True, unique=True)
    username = StringField(required=True, unique=True, max_length=50)
    password = StringField(required=True, min_length=8)
    email = EmailField(required=True, unique=True, max_length=50)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    is_admin = BooleanField(required=True, default=False)
    is_active = BooleanField(required=True)
