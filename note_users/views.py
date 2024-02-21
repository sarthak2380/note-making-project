# views.py

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_routes(request):
    routes = [
        {'POST': '/login'},
        {'POST': '/signup'},
        {'POST': '/notes/create'},
        {'GET': '/notes/<str:id>'},
        {'PUT': '/notes/<str:id>'},
        {'POST': '/notes/share'},
        {'GET': 'notes/version-history/<str:id>'}
    ]

    return Response(routes)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=make_password(serializer.validated_data['password']))
            return Response({'message': 'Registration successful'}, status=201)
        return Response({'error': serializer.errors}, status=400)
    else:
        return Response({'error': 'Invalid request method'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    else:
        return Response({'error': 'Invalid request method'}, status=400)
