from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
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
      



class PostView(ViewSet):

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
        new_post.image_path = request.data["image_path"]
     

        new_post.save()

        serialized = PostSerializer(new_post, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    