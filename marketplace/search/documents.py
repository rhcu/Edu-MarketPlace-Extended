from courses.models import Course
from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter

# Elasticsearch text analyzer = tokenizer + character filters + token filters
courses_analyzer = analyzer(
    'courses_analyzer',
    tokenizer="standard",
    filter=[
        "lowercase",
        "stop",
        "snowball"
    ],
    char_filter=["html_strip"]
)

users_analyzer = analyzer(
    'users_analyzer',
    tokenizer='whitespace',
    filter=[
        'lowercase',
        token_filter('ascii_fold', 'asciifolding')
    ]
)


courses = Index('course')
courses.settings(
    number_of_shards=1,
    number_of_replicas=1
)

users = Index('user')
users.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@registry.register_document
@courses.doc_type
class CourseDocument(Document):
    """Course ElasticSearch document."""
    id = fields.IntegerField(attr='id')

    title = fields.TextField(
        analyzer=courses_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    description = fields.TextField(
        analyzer=courses_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    topic = fields.TextField(
        analyzer=courses_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    owner = fields.TextField(
        attr='owner_indexing',
        analyzer=courses_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    date_created = fields.DateField()

    price = fields.FloatField()

    visible = fields.BooleanField()

    rating = fields.FloatField()

    class Django(object):
        """Inner nested class Django."""
        model = Course  # The model associated with this Document


@registry.register_document
@users.doc_type
class UserDocument(Document):
    """User ElasticSearch document."""
    id = fields.IntegerField(attr='id')

    username = fields.TextField(
        analyzer=users_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    first_name = fields.TextField(
        analyzer=users_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    last_name = fields.TextField(
        analyzer=users_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    email = fields.TextField(
        analyzer=users_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    class Django(object):
        """Inner nested class Django."""
        model = User  # The model associated with this Document
