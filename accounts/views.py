from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, User
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, LoginSerializer
from .permissions import UserCanWriteOrReadOnly
from accounts.serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class CreateUserView(APIView):
    get_token = dict

    def post(self, request):
        ser_data = UserSerializer(data=request.data,)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            user = User.objects.create_user(
                phone_number=cd['phone_number'],
                email=cd['email'],
                full_name=cd['full_name'],
                password=cd['password1'],
            )
            return Response({
                'token': user.get_token()})
        return Response(ser_data.errors)


class UserLogin(APIView):
    """
    the login class give the user token for save it in user cookie
    """
    def post(self, request):
        ser_data = LoginSerializer(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user:
                token = Token.objects.get(user=user)
                return Response({
                    'token': token.key
                })

            return Response({
                'error': 'password or phone_number is wrong'
            })
        return Response(ser_data.errors)


class AccountsView(APIView):
    """
        this class just show the user Accounts
        need to redirect user to this class after login to choose witch account that they want
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        accounts = user.auser.all()
        ser_data = AccountSerializer(instance=accounts, many=True)
        return Response(ser_data.data)


class CreateAccountView(APIView):
    """
    send users to this class if they do not have any accounts or wants to make more
    and make sure that the user be authenticated
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = AccountSerializer(data=request.data)
        if ser_data.is_valid():
            if request.user.get_count_account() < 5:
                cd = ser_data.validated_data
                Account.objects.create(
                    user=request.user,
                    profile_image=cd['profile_image'],
                    account_name=cd['account_name'],
                    bio=cd['bio']
                )
                return Response(ser_data.data)
            return Response({
                'limit_access': 'you cant make account more than 5'
            })
        return Response(ser_data.errors)


class ChangeAccountView(APIView):
    """
    with this class users can change their own profile data
    notice : need to be authenticated and the owner of object
    """

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def put(self, request):
        account = get_object_or_404(Account, pk=request.account_id)
        self.check_object_permissions(request, account)
        ser_data = AccountSerializer(instance=account, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class DeleteAccountView(APIView):

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def delete(self, request, account_id):
        profile = Account.objects.get(id=account_id)
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response({
            'delete': 'you delete your account successfully'
        })


