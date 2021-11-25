from .models import Document, DocumentAccess, User
from .serializers import AddDocumentAccessSerializer, DocumentSerializer, RegistrationRequestSerializer, LoginRequestSerializer, LoginResponseSerializer, UserSerializer, DocumentRequestSerializer
from rest_framework.views import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.serializers import ValidationError
from .exceptions import HealthWealthException
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from .models import Document
from .services import DocumentAccessService, DocumentService
from rest_framework.parsers import MultiPartParser


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not IsAuthenticated().has_permission(request, view)


class EditUserView(GenericAPIView):

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class RegistrationView(GenericAPIView):

    permission_classes = (IsNotAuthenticated, )
    serializer_class = RegistrationRequestSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        request_serializer = self.serializer_class(data=request.data)
        try:
            request_serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if 'email' in e.detail and e.detail['email'][0].code == 'unique':
                return Response({
                    'code': 'Email used',
                    'detail': 'Account with specified email is already registered.',
                }, status=status.HTTP_400_BAD_REQUEST)
            raise e

        with transaction.atomic():
            user = User.objects.create_user(
                email=request_serializer.validated_data['email'].lower(),
                password=request_serializer.validated_data['password'],
                full_name=request_serializer.validated_data['full_name'],
            )

        return Response({
            'code': 'Registration successful',
            'detail': {'full_name': user.full_name, 'email': user.email},
        })


class LoginView(TokenObtainPairView):
    permission_classes = (IsNotAuthenticated, )
    serializer_class = LoginRequestSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except HealthWealthException as e:
            return e.as_response()

        data = serializer.validated_data
        return Response(LoginResponseSerializer(data).data, status=status.HTTP_200_OK)


class UploadDocumentView(GenericAPIView):
    serializer_class = DocumentRequestSerializer
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            documentService = DocumentService()

            uploaded_file = documentService.save_file(
                request.user,
                serializer.validated_data['file'],
                serializer.validated_data['title'],
                serializer.validated_data['description'],
                serializer.validated_data['issuername'],
                serializer.validated_data['issueddate'],
                serializer.validated_data['category'],
            )

            return Response(DocumentSerializer(uploaded_file).data)
        else:
            return Response({
                'code': 'file_error',
                'detail': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class ListDocumentView(ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        documents_granted = DocumentAccess.objects.filter(user=self.request.user).values_list('document_id', flat=True)
        return Document.objects.filter(id__in=documents_granted.order_by('-access_granted_date'))

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)


class AddDocumentAccessView(GenericAPIView):
    serializer_class = AddDocumentAccessSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            documentAccessService = DocumentAccessService()
            try:
                documentAccessService.grant_document_access(
                    serializer.validated_data['email'],
                    serializer.validated_data['document_id']
                )
                return Response({'code': "success", 'detail': 'Viewer successfully added'})
            except Exception as e:
                return Response({
                    'code': 'access_error',
                    'detail': str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'code': 'access_error',
                'detail': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
