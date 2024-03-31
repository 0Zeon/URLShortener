from rest_framework import serializers
from .models import ShortLink

class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ['id', 'originUrl', 'shortUrl', 'hash', 'createdAt', 'isDeleted']
