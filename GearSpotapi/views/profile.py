from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
import uuid
import base64
from GearSpotapi.models import Profile, Post, Like
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_at', 'image_path')

class ProfileLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("post", )

        depth = 1


# from GearSpotapi.models import User

class ProfileSerializer(serializers.ModelSerializer):
    user_posts = serializers.SerializerMethodField()
    user_likes = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "profile_image",
            "bio",
            "created_at",
            "user_posts",
            "user_likes"
        )
        depth = 1

    def get_user_posts(self, obj):
        # Get all posts created by this user
        posts = Post.objects.filter(user=obj.user).order_by('-created_at')
        # You can limit the number of posts returned if needed
        # posts = posts[:10]  # Only return the 10 most recent posts
        return ProfilePostSerializer(posts, many=True, context=self.context).data

    def get_user_likes(self, obj):
        likes = Like.objects.filter(user=obj.user).order_by('-created_at')
        return ProfileLikeSerializer(likes, many=True, context=self.context).data

@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(ViewSet):


    permission_classes = [AllowAny]
    

    def list(self, request):
        profiles = Profile.objects.all()

        serializer = ProfileSerializer(
            profiles, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(
            profile, many=False, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):
        new_profile = Profile()
        # Set bio if provided, otherwise set empty string
        new_profile.bio = request.data.get("bio", "")
        new_profile.user = request.auth.user
        new_profile.save()

        # Handle profile image if provided
        if "profile_image" in request.data and request.data["profile_image"] and ';base64,' in request.data["profile_image"]:
            try:
                format, imgstr = request.data["profile_image"].split(";base64,")
                ext = format.split("/")[-1]
                data = ContentFile(
                    base64.b64decode(imgstr),
                    name=f'profile_{new_profile.id}_{uuid.uuid4()}.{ext}', 
                )
                new_profile.profile_image = data
                new_profile.save()  # Save again with the image
            except Exception as e:
                # Log the error but don't crash
                print(f"Error processing profile image: {e}")

        serialized = ProfileSerializer(new_profile, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=False)
    def current_user_profile(self, request):
        """Get the profile of the currently logged-in user"""
        try:
            current_profile = Profile.objects.get(user=request.auth.user)
            serializer = ProfileSerializer(
                current_profile, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"message": "Profile not found for current user"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(csrf_exempt)
    @action(methods=["put"], detail=False)
    def update_current_user_profile(self, request):
        """Update the profile of the currently logged-in user"""
        try:
            # Get the current user's profile
            current_profile = Profile.objects.get(user=request.auth.user)
            
            # Update the bio if provided
            if "bio" in request.data:
                current_profile.bio = request.data["bio"]
            
            # Handle profile image update if provided
            if "profile_image" in request.data and request.data["profile_image"] and ';base64,' in request.data["profile_image"]:
                try:
                    format, imgstr = request.data["profile_image"].split(";base64,")
                    ext = format.split("/")[-1]
                    data = ContentFile(
                        base64.b64decode(imgstr),
                        name=f'profile_{current_profile.id}_{uuid.uuid4()}.{ext}', 
                    )
                    # Remove old image if exists
                    if current_profile.profile_image:
                        current_profile.profile_image.delete(save=False)
                    
                    current_profile.profile_image = data
                except Exception as e:
                    # Log the error but don't crash
                    print(f"Error processing profile image: {e}")
            
            # Save the updated profile
            current_profile.save()
            
            # Return the updated profile
            serializer = ProfileSerializer(
                current_profile, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Profile.DoesNotExist:
            return Response(
                {"message": "Profile not found for current user"}, 
                status=status.HTTP_404_NOT_FOUND)

  
