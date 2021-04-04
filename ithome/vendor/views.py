from django.shortcuts import render
from .models import Vendor
# 額外 import Http404
from django.http import Http404
from django.shortcuts import get_object_or_404 # 新增
from .forms import RawVendorForm, VendorForm, VendorModelForm # 新增 RawVendorForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView# 新增


# Create your views here.
# 繼承 ListView
class VendorListView(ListView):
    model = Vendor
    template_name = 'vendor_list.html'

# 繼承 DetailView
class VendorDetailView(DetailView):
    model = Vendor
    # queryset = Vendor.objects.all()
    template_name = 'vendor_detail.html'

class VendorCreateView(CreateView):
    form_class = VendorModelForm
    # model = Vendor
    # fields=['vendor_name', 'store_name']
    template_name = 'vendor_create.html'


class VendorUpdateView(UpdateView):
    form_class = VendorModelForm
    template_name = 'vendor_create.html'
    queryset = Vendor.objects.all() # 這很重要

# # Create your views here.
# def showtemplate(request):
#     vendor_list = Vendor.objects.all()
#     context = {'vendor_list': vendor_list}
#     # print(vendor_list)
#     return render(request, 'vendor_detail.html', context)

# def singleVendor(request, id):
#     vendor_one = get_object_or_404(Vendor, id=id)
#     # try:
#     #     vendor_one = Vendor.objects.get(id=id)
#     # except Vendor.DoesNotExist:
#     #     raise Http404
#     context = {
#         'vendor_one': vendor_one
#     }
#     return render(request, 'vendor_detail_one.html', context)

# def vendor_create_view(request):
#     form = RawVendorForm(request.POST or None)
#     if form.is_valid():
#         Vendor.objects.create(**form.cleaned_data) # 新增
#         form = RawVendorForm()
#     context = {
#         'form' : form
#     }
#     return render(request, "vendor_create.html", context)

# # 針對 vendor_create.html
# def vendor_create_view(request):
#     form = VendorForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = VerdorForm() # 清空 form

#     context = {
#         'form' : form
#     }
#     return render(request, "vendor_create.html", context)
