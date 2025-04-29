from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.core.files.base import ContentFile
import uuid
import base64
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Post
from GearSpotapi.models import User
from GearSpotapi.models import Comment
from GearSpotapi.models import PostTag
from GearSpotapi.models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "post",
            "user",
            "created_at")
        depth = 1

class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ('post', 'tag')
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'created_at')
        depth = 1

class PostSerializer(serializers.ModelSerializer):
    post_comments = serializers.SerializerMethodField()
    post_tags = serializers.SerializerMethodField()
    post_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "description",
            "created_at",
            "updated_at",
            "image_path",
            "post_comments", 
            "post_tags",
            "post_likes"
        )
        depth = 1
    
    def get_post_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data

    def get_post_tags(self, obj):
        post_tags = PostTag.objects.filter(post=obj)
        return PostTagsSerializer(post_tags, many=True).data

    def get_post_likes(self, obj):
        likes = Like.objects.filter(post=obj)
        return LikeSerializer(likes, many=True).data


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

    