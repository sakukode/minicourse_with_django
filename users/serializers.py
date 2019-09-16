from django.contrib.auth.models import Group, User
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    #for member
    is_author = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'groups', 'password', 'is_author']
        read_only_fields = ['username', 'date_joined']

    def create(self, validated_data):
        is_author = validated_data.pop('is_author')

        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
        )

        if is_author is True:
            author_group = Group.objects.get(name="author")

            if author_group:
                author_group.user_set.add(user)

        return user