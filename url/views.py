from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import ShortLink
from .serializers import ShortLinkSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class CreateShortLinkView(APIView):
    @swagger_auto_schema(
        operation_id="Short Link 생성",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['originUrl'],
            properties={
                'originUrl': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI)
            }
        ),
        responses={
            status.HTTP_201_CREATED: ShortLinkSerializer,
            status.HTTP_400_BAD_REQUEST: 'Short URL 생성 실패하였습니다.'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ShortLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowAllLinksView(APIView):
    @swagger_auto_schema(
        operation_id="전체 Links 조회",
        responses={
            status.HTTP_200_OK: ShortLinkSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'URL 조회 실패하였습니다.'
        }
    )
    def get(self, request):
        try:
            short_links = ShortLink.objects.filter(isDeleted=False).order_by('-createdAt')
            serializer = ShortLinkSerializer(short_links, many=True)
        except short_links.DoesNotExist:
            return Response({"message":"URL 조회 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteShortLinkView(APIView):
    @swagger_auto_schema(
        operation_id="Short Link 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: 'URL 삭제 성공하였습니다.',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'URL 삭제 실패하였습니다.'
        }
    )
    def delete(self, request, shortlink_id, *args, **kwargs):
        try:
            short_link = ShortLink.objects.get(id=shortlink_id)
            short_link.delete()
        except ShortLink.DoesNotExist:
            return Response({"message":"URL 삭제 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message":"URL 삭제 성공하였습니다."}, status=status.HTTP_204_NO_CONTENT)

class RedirectShortLinkView(APIView):
    @swagger_auto_schema(
        operation_id="Short Link 리다이렉트",
        responses={
            status.HTTP_200_OK: '원본 URL 조회 성공하였습니다.',
            status.HTTP_500_INTERNAL_SERVER_ERROR: '원본 URL 조회 실패하였습니다.'
        }
    )
    def get(self, request, hash, *args, **kwargs):
        try:
            short_link = ShortLink.objects.get(hash=hash, isDeleted=False)
            return redirect(short_link.originUrl)
        except ShortLink.DoesNotExist:
            return Response({"message": "원본 URL 조회 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
