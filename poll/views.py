from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveAPIView,DestroyAPIView
from poll.serializers import UserSerializer,PollSerialiser,ChoiceSerializer,VoteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from poll.models import *
from rest_framework import serializers
# Create your views here.

class UserCreateView(CreateAPIView):
    serializer_class=UserSerializer

class PollView(ListCreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerialiser
    queryset=POll.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class PollListView(ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerialiser
    queryset=POll.objects.all()


class PollRetrieveView(RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerialiser
    queryset=POll.objects.all()


class PollDeleteView(DestroyAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=PollSerialiser
    queryset=POll.objects.all()
    
class ChoiceView(CreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=ChoiceSerializer

    def perform_create(self, serializer):
        poll_id=self.kwargs.get("pk")
        pollobj=POll.objects.get(id=poll_id)
        return serializer.save(poll_obj=pollobj)

class VoteCreateView(CreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=VoteSerializer

    def perform_create(self, serializer):
        pid=self.kwargs.get('pk')
        poll_obj=POll.objects.get(id=pid)
        valid_choice_obj=Choices.objects.filter(poll_obj=poll_obj)
        choice_obj=serializer.validated_data.get('choice_obj')
        # choice_obj=Choices.objects.get(id=choice_id)
        if choice_obj not in valid_choice_obj:
            raise serializer.ValidationError("This is not in poll")
        return serializer.save(poll_obj=poll_obj,owner_obj=self.request.user)