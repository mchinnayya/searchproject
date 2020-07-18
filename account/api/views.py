from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator

from account.api.serializers import UserSerializer, AccountSerializer
from account.models import Account
from django.db.models import Q
from django.core.serializers import serialize


@api_view(['GET', 'POST'])
def account_list(request):
    if request.method == 'GET':
        queryset = Account.objects.all().order_by('-id')
        query = request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
            ).distinct()
        paginator = Paginator(queryset, 2)  # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        serializer = AccountSerializer(contacts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            # user_serializer.save()
            user = User()
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.password = make_password(request.POST.get('password'), None)
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.date_joined = request.POST.get('date_joined')
            user.save()

            profile = Account()
            profile.user = user
            profile.organization = Organization.objects.get(id=1)
            profile.mobile = request.POST.get('mobile')
            profile.full_name = request.POST.get(
                'first_name') + " " + request.POST.get('last_name')
            profile.start_date = request.POST.get('start_date')
            profile.end_date = request.POST.get('end_date')
            profile.user_role = request.POST.get('user_role')
            profile.user_picture = "test"
            profile.gender = request.POST.get('gender')
            profile.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

