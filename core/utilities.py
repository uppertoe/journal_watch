from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.http import JsonResponse


class ExtendedEncoder(DjangoJSONEncoder):
    """
    Allows model objects to be passed to the json encoder
    Works with JsonResponse, json.dumps
    """
    def default(self, o):

        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        is_ajax = self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if not is_ajax:
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        is_ajax = self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if not is_ajax:
            return response
        else:
            return JsonResponse({'response': self.object.pk})
