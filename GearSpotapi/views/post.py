from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.files.base import ContentFile
import uuid
import base64
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Post
from GearSpotapi.models import User

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

    permission_classes = [AllowAny]

    def list(self, request):

        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post =Post.objects.get(pk=pk)
        serializer = PostSerializer(
            post, many=False, context={"request": request}
        )
        return Response(serializer.data)
    
    def create(self, request):
       

        new_post = Post()
        new_post.title = request.data["title"]
        new_post.user = request.auth.user
        new_post.description = request.data["description"]
        if "image_path" in request.data:
            format, imgstr = request.data["image_path"].split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'{new_post.id}-{request.data["name"]}-{uuid.uuid4()}.{ext}',
            )

            new_post.image_path = data
     

        new_post.save()

        serialized = PostSerializer(new_post, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    