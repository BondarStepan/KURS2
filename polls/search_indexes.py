import datetime
from haystack import indexes
from .models import compendium


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    users = indexes.CharField(model_attr='users')
    change_date = indexes.DateTimeField(model_attr='change_date')

    def get_model(self):
        return compendium

    def index_queryset(self, using=None):
        return self.get_model().objects.all()