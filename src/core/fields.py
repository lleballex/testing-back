from rest_framework.serializers import SerializerMethodField


class WriteSerializerMethodField(SerializerMethodField):
	"""Not read only SerializerMethodField"""

	def __init__(self, method_name=None, **kwags):
		super().__init__(method_name, **kwags)
		self.read_only = False

	def to_internal_value(self, data):
		if hasattr(self.parent, f'get_data_{self.field_name}'):
			data = getattr(self.parent, f'get_data_{self.field_name}')(data)
		return {self.field_name: data}