from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Tag
from GearSpotapi.models import PostTag

class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ('post', 'tag')
        depth = 1

class TagSerializer(serializers.ModelSerializer):
    post_tags = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = (
            "name",
            "post_tags"
        )
        depth = 1

    def get_post_tags(self, obj):
        post_tags = PostTag.objects.filter(tag=obj)
        return PostTagsSerializer(post_tags, many=True).data


class TagView(ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags, many=True, context={"request": request}
        )
        return Response(serializer.data)
