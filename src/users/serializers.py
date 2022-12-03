from rest_framework import exceptions, fields, serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = fields.EmailField(required=True)
    confirm_password = serializers.CharField(required=True, max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ["uuid", "first_name", "last_name", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise exceptions.ValidationError(f"Email {email} already exists")
        return email

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        del validated_data["confirm_password"]

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserTokenSerializer(serializers.Serializer):
    email = fields.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=200)
