from django.urls import path
from .views import CreateShortLinkView

urlpatterns = [
    path('short-links', CreateShortLinkView.as_view(), name='create_short_link'),
]
