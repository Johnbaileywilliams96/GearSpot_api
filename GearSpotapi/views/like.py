from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Comment
from GearSpotapi.models import Post
from GearSpotapi.models import User
from GearSpotapi.models import Like



class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = (
            "post",
            "user",
            "created_at"
        )



class LikeView(ViewSet):

    permission_classes = [AllowAny]

    def list(self, request):

        likes = Like.objects.all()

        serializer = LikeSerializer(
            likes, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        like = Like.objects.get(pk=pk)
        serializer = LikeSerializer(
            like, many=False, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):

        new_like = Like()

        new_like.save()

        serialized = LikeSerializer(new_like, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
