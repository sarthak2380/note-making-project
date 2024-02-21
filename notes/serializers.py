# serializers.py in your notes app

from rest_framework import serializers
from .models import Note, NoteChange, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    shared_with = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner', 'shared_with', 'created_at']

class NoteChangeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = NoteChange
        fields = ['timestamp', 'changes_to_title', 'changes_to_content', 'user']
