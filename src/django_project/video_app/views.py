from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.application.use_cases import (
    CreateVideoWithoutMedia,
    ListVideo,
    UploadVideo,
    GetVideo,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    ListVideoResponseSerializer,
    CreateVideoRequestSerializer,
    DeleteVideoRequestSerializer,
    CreateVideoResponseSerializer,
    RetrieveVideoRequestSerializer,
    RetrieveVideoResponseSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "title")
        use_case = ListVideo(
            repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
            genre_repository=DjangoORMGenreRepository()
        )
        input = ListVideo.Input(
            order_by=order_by,
            current_page=int(request.query_params.get("current_page", 1)),
        )
        output = use_case.execute(input)
        serializer = ListVideoResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request,  pk: UUID = None) -> Response:
        serializer = RetrieveVideoRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetVideo(
            repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
            genre_repository=DjangoORMGenreRepository()
        )

        try:
            output = use_case.execute(GetVideo.Input(id=serializer.validated_data["id"]))
        except VideoNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Video with id {pk} not found"},
            )

        video_output = RetrieveVideoResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK,data=video_output.data)

    def create(self, request: Request) -> Response:
        serializer = CreateVideoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVideoWithoutMedia.Input(**serializer.validated_data)
        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
            genre_repository=DjangoORMGenreRepository()
        )
        output = use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateVideoResponseSerializer(output).data,
        )

    def update(self, request: Request, pk: UUID = None):
        raise NotImplementedError

    def partial_update(self, request: Request, pk: UUID = None):
        file = request.FILES["video_file"]
        content = file.read()
        content_type = file.content_type

        upload_video = UploadVideo(
            repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage(),
            message_bus=MessageBus()
        )
        try:
            upload_video.execute(
                UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name,
                    content=content,
                    content_type=content_type
                )
            )
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)
    
    def destroy(self, request: Request, pk: UUID = None):
        # request_data = DeleteVideoRequestSerializer(data={"id": pk})
        # request_data.is_valid(raise_exception=True)

        # input = DeleteVideo.Input(**request_data.validated_data)
        # use_case = DeleteVideo(repository=DjangoORMVideoRepository())
        # try:
        #     use_case.execute(input)
        # except VideoNotFound:
        #     return Response(status=HTTP_404_NOT_FOUND)

        # return Response(status=HTTP_204_NO_CONTENT)
        raise NotImplementedError