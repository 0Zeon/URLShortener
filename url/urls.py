from django.urls import path
from .views import CreateShortLinkView, ShowAllLinksView, DeleteShortLinkView

urlpatterns = [
    path('short-links', CreateShortLinkView.as_view(), name='create_short_link'),
    path('short-links/all', ShowAllLinksView.as_view(), name='show_all_links'),
    path('short-links/delete/<int:short_id>', DeleteShortLinkView.as_view(), name='delete_short_link'),
]
