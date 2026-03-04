from django.template.defaulttags import URLNode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from book_library.models import Book
from book_library.serializers import BookSerializer, UserRegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BookViewSet(viewsets.ModelViewSet):
    """Defines viewset for book model"""
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['publication_year', 'title']

    def get_permissions(self):
        """
        Retrieve, create, update or delete permissions for permission classes.
        - Delete actions require administrative privileges.
        - All other actions require the user to be authenticated.
        """
        if self.action == "destroy":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Defines permissions required to create a new book"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Defines permissions required to delete a book"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Book '{instance}' has been deleted"},
            status=status.HTTP_200_OK
        )


class UserRegisterView(generics.CreateAPIView):
    """Defines viewset for user model"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
