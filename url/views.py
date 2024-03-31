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

class ShowAllLinksView(APIView):
    def get(self, request):
        try:
            short_links = ShortLink.objects.filter(isDeleted=False)
            serializer = ShortLinkSerializer(short_links, many=True)
        except short_links.DoesNotExist:
            return Response({"message":"URL 조회 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteShortLinkView(APIView):
    def delete(self, request, short_id, *args, **kwargs):
        try:
            short_link = ShortLink.objects.get(id=short_id)
            short_link.delete()
        except ShortLink.DoesNotExist:
            return Response({"message":"URL 삭제 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message":"URL 삭제 성공하였습니다."}, status=status.HTTP_204_NO_CONTENT)
