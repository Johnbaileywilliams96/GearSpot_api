from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Comment
from GearSpotapi.models import Post
from GearSpotapi.models import User
from GearSpotapi.models import Like
from rest_framework.decorators import action



# class LikeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Like
#         fields = (
#             "post",
#             "user",
#             "created_at"
#         )


class LikeView(ViewSet):

    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        try:
            user = request.auth.user
            post_id = request.data.get("post")
            
            if not post_id:
                return Response(
                    {"error": "Post ID is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return Response(
                    {"error": "Post not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        
            like = Like.objects.filter(post=post, user=user).first()

            if like:
        
                like.delete()
                message = "Unliked"
                action_status = "unliked"
            else:
          
                Like.objects.create(
                    post=post,
                    user=user
                )
                message = "Liked successfully"
                action_status = "liked"
            
           
            updated_like_count = Like.objects.filter(post=post).count()
            
            return Response({
                "message": message,
                "status": action_status,
                "likes_count": updated_like_count
            }, status=status.HTTP_200_OK)
            
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)



    # def list(self, request):

    #     likes = Like.objects.all()

    #     serializer = LikeSerializer(
    #         likes, many=True, context={"request": request}
    #     )
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     like = Like.objects.get(pk=pk)
    #     serializer = LikeSerializer(
    #         like, many=False, context={"request": request}
    #     )
    #     return Response(serializer.data)

    # def create(self, request):

    #     new_like = Like()

    #     new_like.save()

    #     serialized = LikeSerializer(new_like, many=False)
    #     return Response(serialized.data, status=status.HTTP_201_CREATED)
