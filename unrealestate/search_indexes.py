from haystack.constants import Indexable
from haystack.indexes import SearchIndex, CharField, EdgeNgramField

from unrealestate.models import Project


class ProjectIndex(SearchIndex, Indexable):
    text = EdgeNgramField(document=True, use_template=True)
    title = CharField(model_attr='title')

    def get_model(self):
        return Project
