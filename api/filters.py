from django_filters import rest_framework as filters

from .models import Follow, Post


class FollowFilter(filters.FilterSet):
    search = filters.NumberFilter(
        field_name='following_id',
        lookup_expr='exact'
    )

    class Meta:
        model = Follow
        fields = ['search']


class PostFilter(filters.FilterSet):
    group = filters.NumberFilter(field_name='group_id', lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['group']
