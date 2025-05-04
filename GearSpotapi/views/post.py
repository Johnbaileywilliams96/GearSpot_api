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
    is_Owner = serializers.SerializerMethodField()

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
            "post_likes",
            "is_Owner"
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
    
    def get_is_Owner(self, obj):
        request = self.context.get("request")
        if request:
            return obj.is_Owner(request)
        return False

  
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
        # Create the post
        new_post = Post()
        new_post.title = request.data["title"]
        new_post.user = request.auth.user
        new_post.description = request.data["description"]
        
        # Save the post first to get an ID
        new_post.save()
        
        # Now handle the image after we have an ID
        if "image_path" in request.data:
            try:
                format, imgstr = request.data["image_path"].split(";base64,")
                ext = format.split("/")[-1]
                data = ContentFile(
                    base64.b64decode(imgstr),
                    name=f'post_{new_post.id}_{uuid.uuid4()}.{ext}', 
                )
                new_post.image_path = data
                new_post.save()  # Save again with the image
            except Exception as e:
                # Log the error but don't crash
                print(f"Error processing image: {e}")
        
        # Handle tags
        try:
            if "tags" in request.data and request.data["tags"]:
                # Ensure it's a list
                tag_ids = request.data["tags"]
                if not isinstance(tag_ids, list):
                    # Try to convert it if it's not a list
                    try:
                        tag_ids = list(tag_ids)
                    except:
                        tag_ids = [tag_ids]
                
                for tag_id in tag_ids:
                    post_tag = PostTag()
                    post_tag.post = new_post
                    post_tag.tag_id = tag_id
                    post_tag.save()
        except Exception as e:
            # Log the error but don't crash
            print(f"Error processing tags: {e}")
        
      
        serialized = PostSerializer(new_post, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            post = Post.objects.get(pk=pk)

         
            if post.user.id != request.auth.user.id:
                return Response(
                    {"message": "You cannot delete a review that is not yours"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            post.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(
                {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, pk=None):
        try:

            post = Post.objects.get(pk=pk)

           
            if post.user.id != request.auth.user.id:
                return Response(
                        {"message": "You cannot update a post that is not yours"},
                    status=status.HTTP_403_FORBIDDEN,
                )
                
            post.title = request.data.get("title", post.title)
            post.description = request.data.get("description", post.description)


            if "image_path" in request.data and request.data["image_path"] and ';base64,' in request.data["image_path"]:
                try:
                    format, imgstr = request.data["image_path"].split(";base64,")
                    ext = format.split("/")[-1]
                    data = ContentFile(
                        base64.b64decode(imgstr),
                        name=f'post_{post.id}_{uuid.uuid4()}.{ext}',
                    )
                    post.image_path = data
                except Exception as e:
                    print(f"Error processing image: {e}")
        
    
            post.save()

            if "tags" in request.data:
                PostTag.objects.filter(post=post).delete()

                if request.data["tags"]:
                    tag_ids = request.data["tags"]
                    if not isinstance(tag_ids, list):
                        try:
                            tag_ids = list(tag_ids)
                        except:
                            tag_ids = [tag_ids]
                    
                    for tag_id in tag_ids:
                        post_tag = PostTag()
                        post_tag.post = post
                        post_tag.tag_id = tag_id
                        post_tag.save()


                serialized = PostSerializer(post,  many=False)
                return Response(serialized.data, status=status.HTTP_200_OK)
            
        except Post.DoesNotExist:
            return Response(
                    {"message": "Post not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
    