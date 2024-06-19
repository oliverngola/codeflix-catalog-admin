from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    ListVideoResponseSerializer,
    CreateVideoRequestSerializer,
    DeleteVideoRequestSerializer,
    CreateVideoResponseSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        # order_by = request.query_params.get("order_by", "name")
        # use_case = ListVideo(repository=DjangoORMVideoRepository())
        # input = ListVideo.Input(
        #     order_by=order_by,
        #     current_page=int(request.query_params.get("current_page", 1)),
        # )
        # output = use_case.execute(input)
        # serializer = ListVideoResponseSerializer(instance=output)

        # return Response(status=HTTP_200_OK, data=serializer.data)
        raise NotImplementedError

    def create(self, request: Request) -> Response:
        serializer = CreateVideoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVideoWithoutMedia.Input(**serializer.validated_data)
        use_case = CreateVideoWithoutMedia(repository=DjangoORMVideoRepository())
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
            storage_service=LocalStorage()
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