from rest_framework import routers
from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
