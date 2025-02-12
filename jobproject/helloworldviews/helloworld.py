from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


class HelloViewSet(viewsets.ViewSet):
    def basic(self, request: Request) -> Response:
        return Response({"message": "Hello World!"})
