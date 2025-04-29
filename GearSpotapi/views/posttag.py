from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import PostTag
# from GearSpotapi.models import User

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = (
            "post",
            "tag"
        )
        depth = 1


class PostTagView(ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        post_tags = PostTag.objects.all()

        serializer = PostTagSerializer(
            post_tags, many=True, context={"request": request}
        )
        return Response(serializer.data)
