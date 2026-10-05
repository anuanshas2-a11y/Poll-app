from rest_framework import serializers
from poll.models import CustomUser
from poll.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["email","username","password","phone","id"]
        read_only_fields=["id"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class PollSerialiser(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True)
    choices=serializers.SerializerMethodField()
    total_vote=serializers.SerializerMethodField()
    class Meta:
        model=POll
        fields="__all__"
        read_only_fields=["created_at","is_active"]

    def get_choices(self,object):
        choice_qs=Choices.objects.filter(poll_obj=object)
        serializer_instance=ChoiceSerializer(choice_qs,many=True)
        return serializer_instance.data

    def get_total_vote(self,object):
        vote_qs=Vote.objects.filter(poll_obj=object)
        return vote_qs.count()


class ChoiceSerializer(serializers.ModelSerializer):
    voters=serializers.SerializerMethodField()
    votes=serializers.SerializerMethodField()
    class Meta:
        model=Choices
        fields="__all__"
        read_only_fields=["id","poll_obj"]

    def get_votes(self,object):
        votes_qs=Vote.objects.filter(choice_obj=object)
        return votes_qs.count()

    def get_voters(self,object):
        votes_qs=Vote.objects.filter(choice_obj=object)
        return votes_qs.values_list('owner_obj__username',flat=True)

class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Vote
        fields="__all__"
        read_only_fields=["id","poll_obj","owner_obj","created_at"]

