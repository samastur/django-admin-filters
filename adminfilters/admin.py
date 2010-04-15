from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.filterspecs import FilterSpec


class GenericFilterSpec(FilterSpec):
    def __init__(self, data, request, title):
        self.data = data
        self.request = request
        self._title = title
        
    def title(self):
        return self._title
        
    def has_output(self):
        return True
        
    def choices(self, changelist):
        if callable(self.data):
            choices = list(self.data())
        else:
            choices = list(self.data)
        for choice in [dict(zip(['selected', 'query_string', 'display'], x)) for x in choices]:
            yield choice
            

class GenericFilterChangeList(ChangeList):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GenericFilterChangeList, self).__init__(request, *args, **kwargs)
          
    @property
    def generic_filters(self):
        return getattr(self.model_admin, 'generic_filters', None)
    
    def build_filter_spec(self, choices, title):
        return GenericFilterSpec(choices, self.request, title)
        
    def get_filters(self, request):
        """
        Extend ChangeList.get_filters to include generic_filters.
        """
        filter_specs = super(GenericFilterChangeList, self).get_filters(request)[0]
        if self.generic_filters:
            for fname in self.generic_filters:
                func = getattr(self.model_admin, fname)
                spec = func(request, self)
                if spec and spec.has_output():
                    filter_specs.append(spec)
        return filter_specs, bool(filter_specs)


class GenericFilterAdmin(ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return GenericFilterChangeList
