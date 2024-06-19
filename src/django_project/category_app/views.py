from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from src.core.category.application.use_cases import (
    CreateCategory,
    DeleteCategory,
    GetCategory,
    ListCategory,
    UpdateCategory
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategory
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer, 
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer
)


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        input = ListCategory.Input(
            order_by=order_by,
            current_page=int(request.query_params.get("current_page", 1)),
        )
        output = use_case.execute(input)
        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request,  pk: UUID = None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(GetCategory.Input(id=serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Category with id {pk} not found"},
            )

        category_output = RetrieveCategoryResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK,data=category_output.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        
        try:
            output = use_case.execute(CreateCategory.Input(**serializer.validated_data))
        except InvalidCategory as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        category_output = CreateCategoryResponseSerializer(instance=output)
        return Response(status=HTTP_201_CREATED,data=category_output.data)

    def update(self, request,  pk: UUID = None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={ **request.data, "id": pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCategory.Input(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Category with id {pk} not found"},
            )
        except InvalidCategory as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(status=HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk: UUID = None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        }, partial=True)
        serializer.is_valid(raise_exception=True)

        input = UpdateCategory.Input(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        
        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Category with id {pk} not found"},
            )
        except InvalidCategory as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(status=HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk: UUID = None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteCategory.Input(**serializer.validated_data)
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Category with id {pk} not found"},
            )

        return Response(status=HTTP_204_NO_CONTENT)
