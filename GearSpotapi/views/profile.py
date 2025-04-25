from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Profile
# from GearSpotapi.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "profile_image",
            "bio",
            "created_at"
        )


class ProfileView(ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        profiles = Profile.objects.all()

        serializer = ProfileSerializer(
            profiles, many=True, context={"request": request}
        )
        return Response(serializer.data)