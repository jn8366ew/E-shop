from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

# load custom models we made
User = get_user_model()


# Associate with DJOSER['SERIALIZERS'] in settings.py
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
