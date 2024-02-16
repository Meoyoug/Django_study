from rest_framework.serializers import ModelSerializer
from .models import User

class MyinfoUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
# Feed에서 노출시킬 User Serializer
class FeedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "is_business")