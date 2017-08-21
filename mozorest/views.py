from __future__ import unicode_literals

import json

import requests
from rest_framework import viewsets, permissions, views
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, AccountSerializer, ExpensesSerializer, TransactionsSerializer, \
    UserDetailsSerializer
from .models import Account, Expenses, UserDetails, Transactions
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(accountUser=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(expenseUser=self.request.user)


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(userId=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(fromUser=self.request.user)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


# class TokenViewSet(views.APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request):
#         print request.data['email']
#         data = request.data['email']
#         if request.data['isvarified']:
#             user = User.objects.get(email=data)
#             token = Token.objects.get(user=user)
#             authtoken = {'bonapacheT': str(token)}
#             return JsonResponse(authtoken)
#         else:
#             return JsonResponse({'error': 'maakda'})

@api_view(['POST'])
def SocialAuthFacebook(request):
    if request.method == 'POST':
        token = request.data['token']
        url = 'https://graph.facebook.com/me?fields=id,name,email,first_name,last_name,picture&access_token=' + token
        r = requests.get(url)
        data = json.loads(r.text)
        if 'error' in data:
            resData = {'error': 'Invalid Auth Token ! Beware this incident will be reported !'}
        else:
            try:
                user = User.objects.get(username=data['email'])
                serializer = UserSerializer(user)
                token = Token.objects.get(user=user)
                userDetail, created = UserDetails.objects.get_or_create(userId=user)
                if created:
                    userDetail.userFacebookId = data['id']
                userDetail.userPicUrl = data['picture']
                userDetailSerializer = UserDetailsSerializer(userDetail)
            except User.DoesNotExist:
                newUser = {'username': data['email'], 'email': data['email'], 'first_name': data['first_name'],
                           'last_name': data['last_name'], 'password': 'shotu123'}
                serializer = UserSerializer(data=newUser)
                if serializer.is_valid():
                    serializer.save()
                    user = User.objects.get(username=serializer.data['email'])
                    userDetail, created = UserDetails.objects.get_or_create(userId=user)
                    if created:
                        userDetail.userFacebookId = data['id']
                    userDetail.userPicUrl = data['picture']
                    userDetail.save()
                    token, created = Token.objects.get_or_create(user=user)
            resData = {'token': token.key, 'userData': serializer.data, 'userDetail': userDetailSerializer.data}
        return Response(resData)


@api_view(['POST'])
def SocialAuthGoogle(request):
    if request.method == 'POST':
        token = request.data['token']
        url = 'https://www.googleapis.com/userinfo/v2/me'
        header = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=header)
        data = json.loads(r.text)
        print data
        if 'error' in data:
            resData = {'Error': 'Invalid Credentials ! This event will be reported'}
        else:
            try:
                user = User.objects.get(username=data['email'])
                serializer = UserSerializer(user)
                token = Token.objects.get(user=user)
            except User.DoesNotExist:
                newUser = {'username': data['email'], 'email': data['email'], 'first_name': data['given_name'],
                           'last_name': data['family_name'], 'password': 'shotu123'}
                serializer = UserSerializer(data=newUser)
                if serializer.is_valid():
                    serializer.save()
                    user = User.objects.get(username=serializer.data['email'])
                    userDetail, created = UserDetails.objects.get_or_create(userId=user)
                    userDetail.userGoogleId = data['id']
                    userDetail.save()
                    token, created = Token.objects.get_or_create(user=user)
            resData = {'token': token.key, 'userData': serializer.data}
        return Response(resData)
