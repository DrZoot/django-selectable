from base import LookupBase
from haystack.query import SearchQuerySet
from django.contrib.contenttypes.models import ContentType

class HaystackLookupBase(LookupBase):
    models = ()
    search_fields = ()

    def get_query(self, request, term):
        sqs = SearchQuerySet()
        if self.search_fields:
            kw = dict([(sf, term) for sf in self.search_fields])
            sqs = sqs.filter_or(**kw)
        else:
            sqs = sqs.filter(autocomplete=term)
        if self.models:
            sqs = sqs.models(*self.models)
        return sqs

    def get_item_label(self, item):
        return str(item.object)

    def get_item_id(self, item):
        return '{}__{}'.format(item.content_type, item.pk)

    def get_item_value(self, item):
        return str(item.object)

    def get_item(self, value):
        content_type, pk = value.split('__')
        app_label, model = content_type.split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        item = content_type.get_object_for_this_type(pk=pk)
        return item