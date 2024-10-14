from wagtail.api.v2.views import PagesAPIViewSet
from rest_framework.response import Response

class PaginasAPIViewSet(PagesAPIViewSet):
    def get_slugs_with_ancestors(self, page):
        slugs = [ancestor.slug for ancestor in page.get_ancestors(inclusive=True).reverse()]
        slugs.append(page.slug)
        slug_path = '/'.join(slugs)
        return slug_path

    def get_serializer_data(self, request):
        data = super().get_serializer_data(request)
        if 'slug' in data:
            page = self.get_object()
            slug_path = self.get_slugs_with_ancestors(page)
            data['slug_path'] = slug_path
        return data

    def retrieve(self, request, pk=None):
        response = super().retrieve(request, pk=pk)
        data = response.data
        if 'slug' in data:
            page = self.get_object()
            slug_path = self.get_slugs_with_ancestors(page)
            data['slug_path'] = slug_path
        return Response(data)

    detail_only_fields = []
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'title',
        'slug',
        'slug_path',
        'first_published_at',
        'parent',
        'site',
        'icono',
        'color',
    ]