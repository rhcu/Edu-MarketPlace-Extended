from django_elasticsearch_dsl import Index, Document
from django_elasticsearch_dsl.registries import registry
from courses.models import Course

courses = Index('course')
users = Index('user')


@registry.register_document
class CourseDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'courses'

    class Django:
        model = Course

        fields = [
            'title',
            'description',
            'topic',
            'id',
        ]
