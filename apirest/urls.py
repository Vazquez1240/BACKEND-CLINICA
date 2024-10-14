from django.urls import path, include
from rest_framework import routers
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from .viewsets import PaginasAPIViewSet

drf_router = routers.DefaultRouter()
wagtailapi_router = WagtailAPIRouter('wagtailapi')


urlpatterns = [
    path(r'users/', include('users.urls')),
]

wagtailapi_router.register_endpoint(r'paginas', PaginasAPIViewSet)
wagtailapi_router.register_endpoint(r'imagenes', ImagesAPIViewSet)
wagtailapi_router.register_endpoint(r'documentos', DocumentsAPIViewSet)

urlpatterns += drf_router.urls