import django
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ModelWithProtectedRelationViewSet(ModelViewSet):
    """
    Try: destroy model with protected relation
    Except: return HttpResponse with status 409

    Example:
        from django.db import models as m

        class A(m.Model):
            param = m.Integerfield()

        class B(m.model):
            arg = m.ForeignKey(A, on_delete=m.Protect)

    Instance A will never delete if it has any protected relations
    """

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except django.db.models.deletion.ProtectedError as e:
            return Response(data={'detail': str(e)},
                            status=status.HTTP_409_CONFLICT)
