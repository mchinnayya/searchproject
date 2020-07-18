from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, DeleteView

from branch.forms import BranchForm
from branch.models import Branch


class BranchList(TemplateView):
    model = Branch
    context_object_name = 'branch_list'
    template_name = 'branch/branch_list.html'
    paginate_by = 25

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-id')

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(

                Q(branch_name__contains=query) |
                Q(branch_code__exact=query)

            ).distinct()
        paginator = Paginator(queryset, 25)  # Show 25 contacts per page

        page = self.request.GET.get('page')
        contacts = paginator.get_page(page)
        return contacts

    def get_context_data(self, **kwargs):
        context = super(BranchList, self).get_context_data(**kwargs)
        context['Branches'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class BranchDetails(DetailView):
    model = Branch
    template_name = 'branch/branch_details.html'

    def get(self, request, pk):
        branch = Branch.objects.get(id=pk)

        context = {
            'branch': branch
        }
        return render(request, self.template_name, context)


class BranchCreate(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branch/branch_create.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        branch = Branch()
        branch.branch_name = self.request.POST.get('branch_name')
        branch.branch_code = self.request.POST.get('branch_code')

        branch.save()
        return redirect('branch:branch_list')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(BranchCreate, self).get_context_data(**kwargs)
        context["form"] = self.form_class
        return context


def branchupdate(request, pk):
    branch = Branch.objects.get(pk=pk)
    form = BranchForm(request.POST or None, instance=branch)

    if request.method == 'POST':

        if form.is_valid():
            branch.branch_name = request.POST.get('branch_name')
            branch.branch_code = request.POST.get('branch_code')
            branch.save()
            return redirect('branch:branch_list')
    else:
        form = BranchForm(instance=branch)
    return render(request, 'branch/branch_update.html', {'form': form, 'pk': pk})


class BranchDelete(DeleteView):
    model = Branch
    template_name = 'branch/branch_delete.html'
    success_url = reverse_lazy('branch:branch_list')
