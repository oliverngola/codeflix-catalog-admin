from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest
)
from src.core.category.application.use_cases.list_category import (
    ListCategory, 
    ListCategoryRequest
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import (
    ListCategoryResponseSerializer, 
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer
)

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()

        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(GetCategoryRequest(id=serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK,data=category_output.data)


