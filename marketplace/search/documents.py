from courses.models import Course
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer


# Elasticsearch text analyzer = tokenizer + character filters + token filters
my_analyzer = analyzer(
    'my_analyzer',
    tokenizer="standard",
    filter=[
        "lowercase",
        "stop",
        "snowball"
    ],
    char_filter=["html_strip"]
)

courses = Index('course')
courses.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@registry.register_document
@courses.doc_type
class CourseDocument(Document):
    """Course ElasticSearch document."""
    id = fields.IntegerField(attr='id')

    title = fields.TextField(
        analyzer=my_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    description = fields.TextField(
        analyzer=my_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    topic = fields.TextField(
        analyzer=my_analyzer,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
            'suggest': fields.CompletionField(multi=True),
        }
    )

    owner = fields.TextField(
        attr='owner_indexing',
        analyzer=my_analyzer,
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

        model = Course  # The model associate with this Document

