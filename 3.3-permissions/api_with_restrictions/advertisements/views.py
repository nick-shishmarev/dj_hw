from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, PermissionDenied, NotAcceptable

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorites
from advertisements.permissions import IsOwnerOrAdmin
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):

    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user = self.request.user
        advertisments = (Advertisement.objects.all()
                         .filter(~Q(status=AdvertisementStatusChoices.DRAFT) | Q(creator=user.id)))
        return advertisments

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['creator__username', 'title', 'description']
    ordering_fields = ['id', 'creator', 'created_at']
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return []

    @action(methods=['get'], detail=False)
    def getfavorits(self, request):
        user = self.request.user
        favs = Favorites.objects.filter(user=user.id).all().values()
        for fav in favs:
            adv_id = fav.pop('advertisement_id')
            adv = Advertisement.objects.get(id=adv_id)
            fav['advertisement'] = {
                'id': adv.id,
                'title': adv.title,
                'creator': {
                    'id': adv.creator.id,
                    'username': adv.creator.username,
                    'first_name': adv.creator.first_name,
                    'last_name': adv.creator.last_name,
                },
                'created_at': adv.created_at,
                'updated_at': adv.updated_at,
                'status': adv.status,
            }
        return Response([fav for fav in favs])

    @action(methods=['post'], detail=True)
    def makefavorits(self, request, pk):
        user = self.request.user
        if Favorites.objects.filter(user=user.id).filter(advertisement=pk).count() > 0:
            raise NotAcceptable(f"Объявление id={pk} уже в избранном")
        # try:
        #     adv = Advertisement.objects.get(id=pk)
        # except:
        #     raise NotFound('Объявление не найдено')

        adv = Advertisement.objects.filter(id=pk).first()
        if not adv:
            raise NotFound('Объявление не найдено')

        if adv.creator == user or adv.status == AdvertisementStatusChoices.DRAFT:
            raise PermissionDenied
        Favorites.objects.create(user=user, advertisement=adv)
        return Response({'status': f"Объявление id={adv.id} добавлено в избранное"})

    @action(methods=['delete'], detail=True)
    def delfavorits(self, request, pk):
        user = self.request.user
        deleted = Favorites.objects.filter(user=user.id).filter(advertisement=pk).first()
        if not deleted:
            raise NotFound('Объявление не найдено в избранном')

        deleted.delete()
        return Response({'status': f"Объявление id={pk} удалено из избранного"})
