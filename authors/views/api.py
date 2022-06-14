from rest_framework.viewsets import ModelViewSet
from .. serializers import AuthorSerializer
from django.contrib.auth import get_user_model


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.all()
        return qs
