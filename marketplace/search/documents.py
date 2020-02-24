from courses.models import Course
from django_elasticsearch_dsl import Index, Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import token_filter, analyzer, tokenizer, Completion, Keyword, Text, Long
from itertools import permutations

# Elasticsearch text analyzer = tokenizer + character filters + token filters
my_analyzer = analyzer(
    'my_analyzer',
    tokenizer=tokenizer("trigram", "nGram", min_gram=3, max_gram=4),
    filter=[
        'standard',
        'lowercase',
        'stop',
        'snowball',
    ],
)

courses = Index('course')
courses.settings(
    number_of_shards=1,
    number_of_replicas=0
)
courses.analyzer(my_analyzer)


@registry.register_document
class CourseDocument(Document):
    # completion field with a custom analyzer
    suggest = Completion(analyzer=my_analyzer)

    def clean(self):
        """
        Automatically construct the suggestion input and weight by taking all
        possible permutation of Course's title as ``input`` and taking their
        rating as ``weight``.
        """
        self.suggest = {
            'input': [' '.join(p) for p in permutations(self.title.split())],
            'weight': self.rating
        }

    class Index:
        # Name of the Elasticsearch index
        name = 'courses'

    class Django:
        # The model associated with this Document
        model = Course

        # The fields indexed in Elasticsearch
        fields = [
            'title',
            'description',
            'topic',
            'id',
            'rating',
        ]
