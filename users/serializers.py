from .models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'surname','image', 'email', 'phone_number','is_active',
                  'is_tutor', 'is_admin', 'created', 'updated', 'password']
        read_only_field = ['is_active']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
