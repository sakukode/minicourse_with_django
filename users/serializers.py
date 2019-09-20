from django.contrib.auth.models import Group, User
from rest_framework import serializers

from helpers.types import USER_GROUP_TYPES


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    #for group field by name
    group_name = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'groups', 'password', 'group_name']
        read_only_fields = ['username', 'date_joined']

    def create(self, validated_data):
        group_name = validated_data.pop('group_name', None)

        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
        )

        # set related group, if group not empty and in list USER_GROUP_TYPES variable constanst
        if group_name in USER_GROUP_TYPES.keys():
            author_group = Group.objects.get(name=USER_GROUP_TYPES[group_name])

            if author_group:
                author_group.user_set.add(user)

        return user