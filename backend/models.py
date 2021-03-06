from mongoengine import Document, StringField, IntField, ListField, ReferenceField, DateTimeField, FloatField, \
    EmbeddedDocument


class Shop(Document):
    meta = {'collection': 'Shop'}
    name = StringField(required=True, max_length=50)
    url = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    total_reviews_count = IntField(required=True, default=0)
    average_review = FloatField(required=True, default=0)
    reviews = ListField(ReferenceField('Review'))

    def _init__(self, name, url, created_at, updated_at, total_reviews_count, average_review, reviews):
        self.name = name
        self.url = url
        self.created_at = created_at
        self.updated_at = updated_at
        self.total_reviews_count = total_reviews_count
        self.average_review = average_review
        self.reviews = reviews


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

class test(Document):
    meta = {'collection': 'test'}
    name = StringField(max_length=50)
    name_id = StringField(unique=True)