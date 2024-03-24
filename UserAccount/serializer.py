from rest_framework import serializers
from .models import userAccountModel

class UserAcountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = userAccountModel
        fields = [
            'name','Email','Phone_no','password'
        ]

    "this create function is used for hash(encript) the password field "
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance