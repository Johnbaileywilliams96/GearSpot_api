from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Comment
from GearSpotapi.models import Post
from GearSpotapi.models import User



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "post",
            "user",
            "content",
            "created_at",
            "updated_at"
        )

        depth = 1




class CommentView(ViewSet):

    permission_classes = [AllowAny]

    def list(self, request):

        comments = Comment.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(
            comment, many=False, context={"request": request}
        )
        return Response(serializer.data)


