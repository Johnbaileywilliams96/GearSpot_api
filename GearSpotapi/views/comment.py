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

    def create(self, request):
        try:
            # Get the post if it's in the request data
            if "post" not in request.data:
                return Response(
                    {"message": "Post ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            post = Post.objects.get(pk=request.data["post"])
            
            new_comment = Comment()
            new_comment.content = request.data["content"]
            new_comment.user = request.auth.user  # Set user (not content)
            new_comment.post = post  # Set the post relationship
            
            new_comment.save()
            
            serialized = CommentSerializer(new_comment, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response(
                {"message": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
