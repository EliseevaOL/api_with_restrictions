# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Advertisement

from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsAuthor


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    # permission_classes = [IsAuthor]

    ordering_fields = ['id']
    ordering = ['id']  # Сортировка по возрастанию id по умолчанию

    def perform_update(self, serializer):
        advertisement = serializer.instance
        if advertisement.creator != self.request.user:
            raise PermissionError("You do not have permission to perform this action.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionError("You do not have permission to perform this action.")

        instance.delete()

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthor(), IsAuthenticated()]
        #   return [permissions.IsAuthenticatedOrReadOnly()]
        return []

    def list(self, request, *args, **kwargs):
        """Получение списка объявлений."""
        print("List view called with request data:", request.data)
        # Вызываем базовый метод list
        return super().list(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.is_staff:
            return Advertisement.objects.all()
        elif self.request.user.is_authenticated:
            queryset = Advertisement.objects.exclude(status='DRAFT')
            drafts = Advertisement.objects.filter(status='DRAFT', creator=self.request.user)
            return queryset | drafts