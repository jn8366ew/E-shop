from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

# 커스텀 유저 모델을 불러온다.
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
