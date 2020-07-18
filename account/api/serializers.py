from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import Account


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="Username", required=True)
    password = serializers.CharField(label="Password", required=True)
    first_name = serializers.CharField(label="First Name", required=True)
    last_name = serializers.CharField(label="Last Name", required=True)
    email = serializers.CharField(label="Email", required=True)
    date_joined = serializers.CharField(label="Date Joined", required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined')


class AccountSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(label="User rolesetting", required=True)
    mobile = serializers.CharField(label="Mobile", required=True)
    start_date = serializers.CharField(label="Start Date", required=True)
    end_date = serializers.CharField(label="End Date", required=True)
    user_picture = serializers.CharField(label="Picture", required=True)
    gender = serializers.CharField(label="Gender", required=False)

    class Meta:
        model = Account
        fields = (
            'id', 'user_role', 'user', 'organization', 'mobile', 'start_date', 'end_date', 'user_picture', 'gender')
        depth = 5  # for finding the foreign key table details
