from rest_framework import serializers


class GenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()


class SetField(serializers.ListField):
    # Outras alternativas:
    # Na view, converter para Set manualmente
    # Utilizar o SerializerMethodField
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateGenreRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField(), required=False)


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)
    categories = SetField(child=serializers.UUIDField(), required=True, allow_empty=True)