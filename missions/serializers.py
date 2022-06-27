from rest_framework import serializers

from .models import *


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"


class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = "__all__"


class DialogSerializerExtended(DialogSerializer):
    character = CharacterSerializer(read_only=True)


class FactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = "__all__"


class ObjectiveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectiveImage
        fields = "__all__"


class ObjectiveSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Objective
        fields = "__all__"


class ObjectiveSerializerExtended(ObjectiveSerializer):
    images = ObjectiveImageSerializer(many=True, read_only=True)


class MissionSerializer(serializers.ModelSerializer):
    objectives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    facts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dialogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = "__all__"


class MissionSerializerExtended(MissionSerializer):
    objectives = ObjectiveSerializer(many=True, read_only=True)
    facts = FactSerializer(many=True, read_only=True)
    dialogs = DialogSerializer(many=True, read_only=True)
