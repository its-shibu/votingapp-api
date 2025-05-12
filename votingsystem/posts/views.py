from django.contrib.auth.models import User
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from .models import Post, Vote, FormData
from .serializers import PostSerializer, VoteSerializer, FormDataSerializer


# Post List & Create
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
    
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(poster=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


# Vote List & Create (per post)
class VoteListCreateView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You have already voted for this post.")
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(voter=self.request.user, post=post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("You have not voted for this post.")


# Form Data List & Create
class FormDataCreateView(generics.ListCreateAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    permission_classes = [permissions.AllowAny]

    # Optionally remove this method to avoid accidental deletion in production
    def delete(self, request, *args, **kwargs):
        FormData.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Form Data Retrieve, Update, Destroy
class FormDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.AllowAny]


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            print(f"Received data: {data}")  # Debug

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not all([username, email, password]):
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Optional: Check for duplicate email
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': str(token)}, status=200)

        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            return JsonResponse({'error': 'Username already exists'}, status=400)

        except Exception as e:
            print(f'Unexpected error: {e}')
            return JsonResponse({'error': 'Invalid request'}, status=400)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(username = data['username'], password = data ['password'])
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status = 400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token), 'username' : user.username, 'password' : user.password}, status = 200)