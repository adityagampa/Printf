from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.template import loader

from printf.models import Customers
from printf.models import Merchants
from printf.models import Orders
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from printf.forms import *
from queries import display
from datetime import date


@method_decorator(login_required,name='dispatch')
class CustomersCreateView(CreateView):
    model = Customers
    fields = ['id','name','location']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CustomersCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("Printf_createorder")

@method_decorator(login_required,name='dispatch')
class MerchantsCreateView(CreateView):
    model = Merchants
    fields = ['id','name','location','cost']

    def get_success_url(self):
        return reverse("MerchantsListView")

# @method_decorator(login_required,name='dispatch')
# class OrdersCreateView(CreateView):
#     model = Orders
#     fields = ['id','qty','date_of_order','date_of_delivery','customer','merchant']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(OrdersCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("Printf_customerorder")

def handle_uploaded_file(f):
    with open('temp_files/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def list(request,merchant_id):
    if request.method=="POST":
        file = OrderForm(request.POST,request.FILES)

        if file.is_valid():
            handle_uploaded_file(request.FILES['docfile'])
            customers=Customers.objects.get(user_id=request.user)
            order=file.save(commit=False)
            order.date_of_order=date.today()
            order.merchant = Merchants.objects.get(id=merchant_id)
            order.customer=customers
            order.save()
            return HttpResponseRedirect(reverse('Printf_customerorder'))
    else:
        file=OrderForm()
        # file = DocumentForm()
    # images=Orders.objects.values_list('qty','date_of_order','date_of_delivery','customer','merchant')
    # files = Orders.objects.values_list('doc_file')

    return render(request,'printf/orders_form.html',{'myorders':Orders,'form':file})

@method_decorator(login_required,name='dispatch')
class CustomersDetailView(DetailView):
    model = Orders
    context_object_name = 'myorders'

    def get_object(self, queryset=None):
        customer = Customers.objects.filter(pk=self.kwargs.get("customer_id"))
        if customer:
            return Orders.objects.all().filter(customer=customer)
        else:
            userid = self.request.user.id
            customer=Customers.objects.filter(user=userid)
            return Orders.objects.all().filter(customer=customer)

@method_decorator(login_required,name='dispatch')
class OrdersListView(ListView):
    model = Orders
    context_object_name = 'allorders'

    def get_object(self, queryset=None):
            return Orders.objects.all()

@method_decorator(login_required,name='dispatch')
class MerchantsListView(ListView):
    model = Merchants
    context_object_name = 'allmerchants'

    def get_object(self, queryset=None):
            return Merchants.objects.all()

@method_decorator(login_required,name='dispatch')
class MerchantsDetailView(DetailView):
    model = Orders
    template_name = 'printf/merchant_homepage.html'
    context_object_name = 'myorders'

    def get_object(self, queryset=None):
        merchant = Merchants.objects.filter(pk=self.kwargs.get("merchant_id"))
        if merchant:
            return Orders.objects.all().filter(merchant=merchant)
        else:
            userid = self.request.user.id
            merchant = Merchants.objects.filter(user=userid)
            return Orders.objects.all().filter(merchant=merchant)
@method_decorator(login_required,name='dispatch')
class MerchantsUpdateView(UpdateView):
    model = Merchants
    fields = ['id', 'name', 'location', 'cost']
    template_name = 'printf/merchant_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MerchantsUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("Printf_merchantorder")
