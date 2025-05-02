from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
import uuid
import base64
from GearSpotapi.models import Profile
from rest_framework.decorators import action 
# from GearSpotapi.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "profile_image",
            "bio",
            "created_at"
        )
        depth = 1


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

           

  
