from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet

router = DefaultRouter()
router.register(r'fields', FieldViewSet, basename='field')

urlpatterns = router.urls + [
    path('fields/nearby/', FieldViewSet.as_view({'get': 'nearby'}), name='field-nearby'),
    path('fields/inside/', FieldViewSet.as_view({'post': 'inside'}), name='field-inside'),
    path('fields/intersect/', FieldViewSet.as_view({'post': 'intersect'}), name='field-intersect'),
    path('fields/region_stats/', FieldViewSet.as_view({'get': 'region_stats'}), name='field-region-stats'),
]

