from rest_framework.serializers import ModelSerializer
from chatbot.models import Computers

class ComputerSerializer(ModelSerializer):

    class Meta:
        model = Computers
        fields = "__all__"