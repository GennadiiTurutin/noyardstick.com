from rest_framework import viewsets
from .serializers import ( 
    PostSerializer, 
    PostSerializer_, 
    TagSerializer, 
    CategorySerializer,
    CommentSerializer, 
    CommentDetailSerializer,
    UserSerializer, 
    ImageSerializer,
    SubscriberSerializer,
    ArchiveSerializer
    )

from django.contrib.auth.models import User
from .models import MyUser, Post, Tag, Comment, Image, Category, Subscriber, Archive
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    CreateAPIView
    )

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import generics

from django.db.models import Q

from rest_framework.filters import (
    SearchFilter, 
    OrderingFilter
    )

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
    )

from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail

# User - GET, POST

class UserViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer   
    authentication_classes = (TokenAuthentication, )
    permission_classes = ()

# Post - GET, POST

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-date_posted")
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ('title', 'subtitle', 'content')

# Post Long Read - GET

class PostLongReadViewSet(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(long_read=True)

# Post Important - GET

class PostImportantViewSet(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(super_important=True)

# Post for Tag - GET

class PostList(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        tagname = self.kwargs['tagname']
        return Tag.objects.filter(name=tagname)

# Post for Category - GET

class PostListCategory(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Category.objects.filter(name=category)

# Post Archive - GET

class PostListArchive(generics.ListAPIView):
    serializer_class = ArchiveSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Archive.objects.filter(year=year, month=month)

# Tag - GET

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# Category - GET

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Archive - GET

class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

# Comment - GET, POST

class CommentViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all().order_by("-date_posted")
    serializer_class = CommentSerializer

# Comment - GET

class CommentDetailViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-date_posted")
    serializer_class = CommentDetailSerializer

# Image - GET

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

# Subscriber - GET, POST

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = ()

class CustomObtainAuthToken(ObtainAuthToken):
    authentication_classes = (TokenAuthentication, )
    permission_classes = ()
    
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = MyUser.objects.get(id=token.user_id)
        serializer = UserSerializer(user, many=False)

        return Response({'token': token.key, 'user': serializer.data})











