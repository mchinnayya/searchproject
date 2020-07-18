from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from account.forms import AccountForm, UserForm
from account.models import Account


def login_view(request):
    data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            user_detail = User.objects.filter(username__iexact=username).first()
            user_id = user_detail.id
            account_detail = Account.objects.filter(user__exact=user_id).first()
            role = account_detail.role
            request.session['role'] = role
            return redirect('emergency:emergencyDetails_list')
        else:
            data['error'] = "Your email and password didn't match. Please try again."
            return render(request, 'account/account_login.html', data)
    return render(request, 'account/account_login.html')


@login_required(redirect_field_name='my_redirect_field', login_url='/accounts/login')
def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('account:login')


class AccountCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'account/create_user.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):

        account = Account()
        account.user = User.objects.filter(id=self.request.POST.get('user'))
        account.active = self.request.POST.get('active')
        account.role = self.request.POST.get('role')
        account.save()
        return redirect('account:account_create')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'user_form': form})

    def get_context_data(self, **kwargs):
        context = super(AccountCreate,self).get_context_data(**kwargs)
        context["user_form"] = self.form_class
        context["account_form"] = AccountForm()
        return context
