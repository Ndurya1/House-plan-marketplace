from collections import defaultdict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from users.models import SellerProfile

from .models import Catalogue
from .serializers import catalogueSerializer
from .permissions import IsSellerOwnerOrAdmin


class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = catalogueSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'categories']:
            return [AllowAny()]
        return [IsAuthenticated(), IsSellerOwnerOrAdmin()]

    def get_queryset(self):
        queryset = Catalogue.objects.select_related('seller__user').all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category.strip())
        return queryset

    def perform_create(self, serializer):
        seller = SellerProfile.objects.filter(user=self.request.user).first()
        if not seller:
            raise ValidationError(
                {"detail": "Only registered sellers with a profile can list house plans."}
            )
        serializer.save(seller=seller)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        rows = (
            Catalogue.objects
            .exclude(category='')
            .exclude(category_group='')
            .values_list('category_group', 'category')
            .distinct()
        )

        grouped = defaultdict(set)
        for group, category in rows:
            grouped[group].add(category)

        return Response({
            group: sorted(categories)
            for group, categories in sorted(grouped.items())
        })
