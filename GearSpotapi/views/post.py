from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from GearSpotapi.models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "description",
            "created_at",
            "updated_at",
            "image_path"
        )
        depth = 1



class PostView(ViewSet):

    def list(self, request):

        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

