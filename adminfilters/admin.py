from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.options import ModelAdmin
        


class GenericFilterChangeList(ChangeList):        
    @property
    def generic_filters(self):
        return getattr(self.model_admin, 'generic_filters', None)
        
    def get_filters(self, request):
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