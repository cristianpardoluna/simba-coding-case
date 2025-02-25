import os
import json
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from pydantic import BaseModel
from typing import Literal, List
from django.conf import settings
from chatbot.serializer import ComputerSerializer
from chatbot.models import Computers
from openai import OpenAI

def load_cached_conversation() -> list:
    """ Retrieves local cached conversation, defaults to empty list
    """
    if os.path.exists(settings.CACHE_PATH):
        with open(settings.CACHE_PATH, "r") as f:
            return json.load(f)
    return []

def save_cached_conversation(messages) -> None:
    """ Saves messages in .json format in local path
    """
    with open(settings.CACHE_PATH, "w") as f:
        json.dump(messages, f)

class RankingModel(BaseModel):
    id: str
    brand: str
    price: float
    rank: Literal[
        "Altamente Recomendado",
        "Recomendado",
        "No Recomendado"
    ]

class RankingListModel(BaseModel):
    recommendations: List[RankingModel]

class ComputerViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ComputerSerializer
    queryset = Computers.objects.all()

    def list(self, request):
        """ Retrieves RankingListModel based on current
            state of the conversation
        """
        openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            organization=settings.OPENAI_API_ORGANIZATION,
            project=settings.OPENAI_API_PROJECT
        )
        serializer = self.get_serializer(many=True)
        cached_messages = load_cached_conversation()
        computers = self.queryset
        repr_computers = serializer.to_representation(computers)
        completion = openai_client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system",
                "content": f"""Rank the products based on the current conversation messages
                Return the rankings in descending order
                --- {cached_messages}
                --- {repr_computers}"""}
            ],
            response_format=RankingListModel
        )
        ranking_parsed = completion.choices[0].message.parsed
        data_json = json.loads(ranking_parsed.model_dump_json())
        return Response(data=data_json)

    @action(methods=["POST"], detail=False)
    def message(self, request):
        """ Action method to retrieve result of message completion call
        """
        openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            organization=settings.OPENAI_API_ORGANIZATION,
            project=settings.OPENAI_API_PROJECT
        )
        data = request.data
        message = data["message"]
        computers = self.queryset
        serializer = self.get_serializer(many=True)
        repr_computers = serializer.to_representation(computers)
        messages = load_cached_conversation() \
            or [{"role": "system",
            "content": """User speaks spanish, do recommendations based on computer stock.
            do not use markdown return plain text"""}]
        messages.append({
            "role": "user",
            "content": message
        })
        messages.append({
            "role": "system",
            "content": json.dumps(repr_computers)
        })
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        assistant_message = response.choices[0].message.dict()
        messages.append(assistant_message)
        save_cached_conversation(messages)
        return Response(assistant_message)


