from rest_framework import serializers
from .models import Document, User
from rest_framework import exceptions, status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .exceptions import HealthWealthException


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=75)
    email = serializers.EmailField(read_only=True)

    phone_number = serializers.CharField(max_length=20, allow_null=True)
    birth_date = serializers.DateField(allow_null=True)
    address = serializers.CharField(max_length=300, allow_null=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'birth_date', 'address')
        read_only_fields = ('email', )


class RegistrationRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=75)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField()


class LoginRequestSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['email'] = user.email

        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['token'] = str(refresh.access_token)
        except exceptions.AuthenticationFailed:
            raise HealthWealthException(
                detail='Wrong email / password',
                code='K_LOGIN_FAILED',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        data['user'] = UserSerializer(self.user).data
        data['exp'] = refresh.payload['exp']

        return data


class LoginResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    exp = serializers.IntegerField(label='token expiry time')
    token = serializers.CharField(max_length=200)


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    uploaded_by = serializers.CharField(source='uploaded_by.email', read_only=True)

    class Meta:

        model = Document
        fields = "__all__"


class DocumentRequestSerializer(serializers.Serializer):

    file = serializers.FileField()
    title = serializers.CharField(max_length=100)

    description = serializers.CharField(max_length=200, allow_null=True)
    category = serializers.CharField(max_length=100, allow_null=True)

    issuername = serializers.CharField(max_length=100, allow_null=True, required=False)
    issueddate = serializers.DateField(allow_null=True, required=False)


class AddDocumentAccessSerializer(serializers.Serializer):
    email = serializers.EmailField()
    document_id = serializers.UUIDField()
