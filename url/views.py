from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import ShortLink
from .serializers import ShortLinkSerializer

class CreateShortLinkView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ShortLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
