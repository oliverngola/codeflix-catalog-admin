from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request:Request) -> Response:
        return Response(status=HTTP_200_OK, data=[
            {
                "id": "b5944983-7177-4a6e-a72a-26a9f330d20e",
                "name": "Movie",
                "description": "Movie Descriptin",  
                "is_active": True
            },
            {
                "id": "c06803a0-58a0-41bd-9094-b1f14a572e3f",
                "name": "Documentary",
                "description": "Documentary Descriptin",  
                "is_active": True
            }
        ])
