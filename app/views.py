
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author, Message
from .serializers import AuthorSerializer, MessagesSerializer

@api_view(["GET"])
def get_messages(request):
    messages = Message.objects.all().order_by("create_at")
    serializer = MessagesSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_message(request):
    username = request.data.get("username")
    content = request.data.get("content")

    if not username or not content:
        return Response(
            {"error": "username and content are required"}, status=status.HTTP_400_BAD_REQUEST)

    author, _ = Author.objects.get_or_create(name=username)

    serializer = MessagesSerializer(data={"content": content})

    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_profile_picture(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({"error": "author not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AuthorSerializer(author, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_author_by_username(request, username):
    try:
        author = Author.objects.get_or_create(name=username)
    except Author.DoesNotExist:
        return Response({"error": "author not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AuthorSerializer(author,data=request.data, partial=True)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)