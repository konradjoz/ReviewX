from mongoengine import Document, StringField, IntField, ListField, ReferenceField, DateTimeField, BooleanField, \
    FloatField, EmbeddedDocument

class Shop(Document):
    meta = {'collection': 'Shop'}
    name = StringField(required=True, max_length=50)
    url = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    total_reviews_count = IntField(required=True, default=0)
    average_review = FloatField(required=True, default=0)
    reviews = ListField(ReferenceField('Review'))


class Review(EmbeddedDocument):
    meta = {'collection': 'Review'}
    shop = ReferenceField('Shop', required=True)
    author = ReferenceField('User', required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    content_title = StringField(required=True, max_length=50)
    content = StringField(required=True, max_length=1000)
    rating = IntField(required=True, min_value=1, max_value=5)
    helpful_count = IntField(required=True, default=0)


class User(Document):
    meta = {'collection': 'User'}
    user_id = IntField(required=True, unique=True)
    username = StringField(required=True, unique=True, max_length=50)
    password = StringField(required=True, min_length=8)
    email = StringField(required=True, unique=True, max_length=50)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    is_admin = BooleanField(required=True, default=False)
    is_active = BooleanField(required=True)

class test(Document):
    meta = {'collection': 'test'}
    name = StringField(max_length=50)
    name_id = StringField(unique=True)