# views.py

from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Note, NoteChange, User
from .serializers import NoteSerializer, NoteChangeSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            note = serializer.save(owner=request.user)
            return Response({'message': 'Note created successfully', 'note_id': note.id}, status=201)
        return Response({'error': serializer.errors}, status=400)
    else:
        return Response({'error': 'Invalid request method'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            note = serializer.save(owner=request.user)
            shared_users = request.data.get('shared_with', [])
            
            for username in shared_users:
                user = get_object_or_404(User, username=username)
                note.shared_with.add(user)

            return Response({'message': 'Note shared successfully', 'note_id': note.id}, status=200)
        return Response({'error': serializer.errors}, status=400)
    else:
        return Response({'error': 'Invalid request method'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_version_history(request, id):
    note = get_object_or_404(Note, id=id)

    if note.owner != request.user and request.user not in note.shared_with.all():
        return Response({'error': 'Permission denied'}, status=403)

    version_history = NoteChange.objects.filter(note=note)
    serializer = NoteChangeSerializer(version_history, many=True)
    return Response({'version_history': serializer.data}, status=200)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_note(request, id):
    note = get_object_or_404(Note, id=id)
    
    if note.owner != request.user and request.user not in note.shared_with.all():
        return Response({'error': 'Permission denied'}, status=403)

    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response({'message': 'Note retrieved successfully', 'note_content': serializer.data['content']}, status=200)

    if request.method == "PUT":
        serializer = NoteSerializer(note, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            
            timestamp = datetime.now()
            note_change = NoteChange(note=note, timestamp=timestamp, user=request.user, changes_to_title=request.data.get('title'), changes_to_content = request.data.get('content'))
            note_change.save()

            return Response({'message': 'Note updated successfully', 'title': serializer.data['title'], 'content': serializer.data['content']}, status=200)
        return Response({'error': serializer.errors}, status=400)


