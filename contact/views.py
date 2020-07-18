# Create your views here.


import csv
import io
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView

from branch.models import Branch
from common.views import dropdownSearch
from contact.forms import EmergencyDetailsForm
from contact.models import Contact
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
import logging
from django.core import serializers
import numpy as nu
from favorite.models import Favorite, Favorite_link_with_contact


class EmergencyDetailsList(TemplateView):
    model = Contact
    context_object_name = 'emergencyDetails_list'
    template_name = 'contact/emergency_details_list.html'
    paginate_by = 25

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-id')

        query = self.request.GET.get("q")
        query1 = self.request.GET.get("branch")
        # print(query1)
        if query:
            queryset = queryset.filter(
                Q(emergency_name__contains=query) |
                Q(emergency_code__contains=query)
            ).distinct()
        if query1 and query1 != '0':
            queryset = queryset.filter(
                Q(branch__exact=query1)
            ).distinct()
        paginator = Paginator(queryset, 2500)  # Show 25 contacts per page

        page = self.request.GET.get('page')
        contacts = paginator.get_page(page)

        return contacts

    def get_context_data(self, **kwargs):
        branch_id = self.request.GET.get('branch')
        branches = Branch.objects.all()
        # print('branch=', branch_id)
        context = super(EmergencyDetailsList, self).get_context_data(**kwargs)
        context['EmergencyDetails'] = self.get_queryset()
        context['delete_str'] = "emergency:emergencyDetails_delete"
        context['update_str'] = "emergency:emeregcy_update"
        context['refresh_str'] = "emergency:emeregcy_active"
        context['branch_id'] = branch_id
        context['selectDropdown'] = dropdownSearch(branches, branch_id)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    # def post(self, request):
    #     emergency_details = Contact()
    #     emergency_details.branch = Branch.objects.get(id=self.request.POST.get('branch'))
    #     emergency_details.contact_name = self.request.POST.get('contact_name')
    #     emergency_details.extension_number = self.request.POST.get('extension_number')
    #     emergency_details.save()
    #     return redirect('emergencyDetails_create')


class EmergencyDetailsDetails(DetailView):
    model = Contact
    template_name = 'contact/emergency_details_details.html'

    def get(self, request, pk):
        emergency = Contact.objects.get(id=pk)
        context = {
            'emergency': emergency
        }
        return render(request, self.template_name, context)


class EmergencyDetailsCreate(CreateView):
    model = Contact
    form_class = EmergencyDetailsForm
    template_name = 'contact/emergency_details_create.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        emergency_detail = Contact()
        emergency_detail.branch = Branch.objects.get(id=self.request.POST.get('branch'))
        emergency_detail.contact_name = self.request.POST.get('contact_name')
        emergency_detail.extension_number = self.request.POST.get('extension_number')
        emergency_detail.save()
        return redirect('emergency:emergencyDetails_list')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(EmergencyDetailsCreate, self).get_context_data(**kwargs)
        context["form"] = self.form_class
        return context


class EmergencyDetailsDelete(DeleteView):
    model = Contact
    template_name = 'contact/emergency_details_delete.html'
    success_url = reverse_lazy('emergency:emergencyDetails_list')


def emergency_detailsupdate(request, pk):
    emergency = Contact.objects.get(pk=pk)
    form = EmergencyDetailsForm(request.POST or None, instance=emergency)

    if request.method == 'POST':

        if form.is_valid():
            emergency.branch = Branch.objects.get(id=request.POST.get('branch'))
            emergency.contact_name = request.POST.get('emergency_name')
            emergency.extension_number = request.POST.get('emergency_code')
            emergency.save()
            return redirect('emergency:emergencyDetails_list')
    else:
        form = EmergencyDetailsForm(instance=emergency)
    return render(request, 'contact/emergency_details_update.html', {'form': form, 'pk': pk})


def emeregcy_active(request, pk):
    emergency = Contact.objects.get(pk=pk)
    emergency.extension_status = '1'
    emergency.save()
    return '1'


def emergency_upload(request):
    template = "contact/emergency_details_upload.html"
    data = Contact.objects.all()
    prompt = {
        'order': 'Order of the CSV should be , emergency_name, emergency_code,branch_id',
        'emergencies': data
    }
    if request.method == "GET":
        return render(request, template, prompt)

    try:
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please choose CSV file only.')
            return redirect("emergency:emergency_upload")
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            created = Contact.objects.update_or_create(
                extension_status=column[0],
                contact_name=column[1],
                extension_number = column[2],
                # branch_id=Branch.objects.filter(id__iexact=column[3]).first()
                branch_id=column[3]
            )
        context = {}
        return render(request, template, context)
    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))
        return redirect("emergency:emergency_upload")


def emergency_details_search(request):
    if request.method == 'GET':
        queryset = Contact.objects.all().order_by('-id')
        query = request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(emergency_name__icontains=query) |
                Q(emergency_code__icontains=query)
            ).distinct()

        data1 = serializers.serialize("json", queryset)

        return HttpResponse(data1, content_type="application/json")


def favorite_save(request):
    favorite = Favorite()
    if request.method == 'POST':
        favorite.favorite_name = request.POST.get('favorite_name')
        favorite.favorite_description = "this is description"
        favorite.save()
        return redirect('emergency:emergencyDetails_list')
    return redirect('emergency:emergencyDetails_list')


def favorite_contact_save(request):
    favorite_contact = Favorite_link_with_contact()
    if request.method == 'POST':
        favorite_contact.favorite = Favorite.objects.get(id=request.POST.get('favorite'))
        # id_new = request.POST.get('contact_id')
        # print(id_new)
        favorite_contact.contact = Contact.objects.get(id=request.POST.get('contact_id'))
        # print(request.POST.get('contact_id'))

        favorite_contact.save()
        return redirect('emergency:emergencyDetails_list')
    return redirect('emergency:emergencyDetails_list')
