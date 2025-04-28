from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from GearSpotapi.models import Tag
# from GearSpotapi.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
        )


class TagView(ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags, many=True, context={"request": request}
        )
        return Response(serializer.data)
