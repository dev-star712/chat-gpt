from rest_framework.pagination import CursorPagination

class CustomPagination(CursorPagination):
    ordering = '-id'