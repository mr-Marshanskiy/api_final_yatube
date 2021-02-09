from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, Group, Post, Comment, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment

        extra_kwargs = {
            'author': {'required': False},
            'post': {'required': False},
        }


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    def validate(self, data):
        if self.context.get('request').user == data.get('following'):
            raise serializers.ValidationError("Нельзя подписаться на себя")
        return data

    class Meta:
        fields = ['user', 'following']
        model = Follow

        extra_kwargs = {
            'user': {'required': False},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
            )
        ]


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['title']
        model = Group
