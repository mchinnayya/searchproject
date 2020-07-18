from django.shortcuts import render

from favorite.forms import FavoriteForm
from favorite.models import Favorite


def favorite(request):
    favorite_list = Favorite.objects.all()
    my_dict = {'favorite_list': favorite_list}

    return my_dict

def get_favorite_list(request):
   pass


def favorite_form(request):
    form = FavoriteForm()
    my_form = {'form': form}
    if request.method == "POST":
        form = FavoriteForm(request.POST)

        if form.is_valid():
            form.save()

        # return render(request, 'layout/header.html', context=my_form)
        return my_form
    #return render(request, 'layout/header.html', context=my_form)
    return my_form
