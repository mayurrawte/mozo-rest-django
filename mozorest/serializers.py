from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserDetails, Account, Transactions, Expenses


class UserDetailsSerializer(serializers.HyperlinkedModelSerializer):
    userId = serializers.ReadOnlyField(source='userId.username')

    class Meta:
        model = UserDetails
        fields = ('id', 'userFacebookId', 'userGoogleId', 'userPicUrl', 'friends', 'userId')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class TransactionsSerializer(serializers.HyperlinkedModelSerializer):
    fromUser = serializers.ReadOnlyField(source='fromUser.username')
    toUser = serializers.DjangoModelField()

    class Meta:
        model = Transactions
        fields = ('transactionType', 'toUser', 'fromUser', 'transactionAmount', 'transactionStatus')


class ExpensesSerializer(serializers.HyperlinkedModelSerializer):
    expenseUser = serializers.ReadOnlyField(source='expenseUser.username')
    class Meta:
        model = Expenses
        fields = ('__all__')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    accountUser = serializers.ReadOnlyField(source='accountUser.username')

    class Meta:
        model = Account
        fields = ('__all__')

