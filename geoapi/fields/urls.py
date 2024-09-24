from django.urls import path
from .views import NearbyFieldsView, InsideParallelogramView, IntersectingFieldsView

urlpatterns = [
    path('nearby/', NearbyFieldsView.as_view(), name='nearby-fields'),
    path('inside/', InsideParallelogramView.as_view(), name='inside-parallelogram'),
    path('intersect/', IntersectingFieldsView.as_view(), name='intersecting-fields'),
]

