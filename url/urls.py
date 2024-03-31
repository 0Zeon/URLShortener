from django.urls import path
from .views import CreateShortLinkView, ShowAllLinksView

urlpatterns = [
    path('short-links', CreateShortLinkView.as_view(), name='create_short_link'),
    path('short-links/all', ShowAllLinksView.as_view(), name='show_all_links'),
]
