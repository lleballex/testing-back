from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.status import HTTP_404_NOT_FOUND


class BaseAPIView(GenericAPIView):
	"""Base class of GenericAPIView"""

	def dispatch(self, request, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		request = self.initialize_request(request, *args, **kwargs)
		self.request = request
		self.headers = self.default_response_headers

		try:
			self.initial(request, *args, **kwargs)

			if request.method.lower() in self.http_method_names:
				handler = getattr(self, request.method.lower(),
								  self.http_method_not_allowed)
			else:
				handler = self.http_method_not_allowed

			response = handler(request, *args, **kwargs)

		except Http404 as e:
			print(e)
			response = Response({'detail': 'Object not found'},
								status=HTTP_404_NOT_FOUND)
		except Exception as exc:
			response = self.handle_exception(exc)

		self.response = self.finalize_response(request, response, *args, **kwargs)
		return self.response