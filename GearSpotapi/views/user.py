from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from GearSpotapi.models import Post  # Import the Post model

class PostListSerializer(serializers.ModelSerializer):
    """Simplified Post serializer for listing purposes"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_at', 'image_path')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializers
    """
    user_posts = serializers.SerializerMethodField() 

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'user_posts')

    def get_user_posts(self, obj):
        """Method to get all posts for a user"""
        # Get all posts created by this user
        posts = Post.objects.filter(user=obj).order_by('-created_at')
        # Serialize them with the simplified serializer
        return PostListSerializer(posts, many=True, context=self.context).data

class UserView(ViewSet):
    """Users for Bangazon
    Purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE Users.
    Methods: GET PUT(id) POST
"""
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Purpose: Allow a user to communicate with the Bangazon database to retrieve  one user
        Methods:  GET
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def list(self, request):
        """Handle GET requests to user resource"""
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)