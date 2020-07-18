from urllib import request

from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import CreateView, TemplateView, DetailView

from contact.models import Contact
from favorite.forms import FavoriteForm
from common.context_processors import get_favorite_list
from favorite.models import Favorite, Favorite_link_with_contact


class Favorite_Contact_Create(CreateView):
    model = Favorite_link_with_contact
    template_name = 'fevorite/fevorite_details_list.html'

    def post(self, request, args, *kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        favorite_contact = Favorite_link_with_contact()
        favorite_contact.favorite = Favorite.objects.get(id=self.request.POST.get('favorite'))
        favorite_contact.contact = Contact.objects.get(branch_id=1)


        favorite_contact.save()
        return redirect('favorite:favorite_contact_create')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(Favorite_Contact_Create, self).get_context_data(**kwargs)
        context["form"] = self.form_class
        return context

class FavoriteDetails(DetailView):
    model = Favorite
    template_name = 'fevorite/fevorite_details_list.html'

    def get(self, request, id):
        favorite = Favorite.objects.get(id=id)
        favorite_contact = Favorite_link_with_contact.objects.filter(favorite_id=id).all()

        context = {
            'favorite_contact': favorite_contact,
            'favorite': favorite,
        }

        return render(request, self.template_name,context)



