from rest_framework import serializers

class DynamicFieldsSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None) 
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)