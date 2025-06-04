from rest_framework import serializers

from src.core.video.domain.value_objects import Rating


class VideoRatingField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in Rating]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return Rating(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))


class VideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    year_launched = serializers.IntegerField()
    opened = serializers.BooleanField()
    rating = VideoRatingField(required=True)
    duration = serializers.IntegerField()
    link = serializers.CharField()
    categories = serializers.ListField(child=serializers.UUIDField())
    genres = serializers.ListField(child=serializers.UUIDField())
    cast_members = serializers.ListField(child=serializers.UUIDField())
    banner_file_url = serializers.CharField()
    thumb_file_url = serializers.CharField()
    video_file_url = serializers.CharField()
    

class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListVideoResponseSerializer(serializers.Serializer):
    data = VideoResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()

class RetrieveVideoRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveVideoResponseSerializer(serializers.Serializer):
    data = VideoResponseSerializer(source="*")


class SetField(serializers.ListField):
    # Outras alternativas:
    # Na view, converter para Set manualmente
    # Utilizar o SerializerMethodField
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateVideoRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    opened = serializers.BooleanField(default=False)
    rating = VideoRatingField(required=True)
    duration = serializers.IntegerField()
    categories = SetField(child=serializers.UUIDField(), required=False)
    genres = SetField(child=serializers.UUIDField(), required=False)
    cast_members = SetField(child=serializers.UUIDField(), required=False)


class CreateVideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteVideoRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

