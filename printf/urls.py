from django.conf.urls import url

import classviews
from . import views
from App import settings
from django.conf.urls.static import static

urlpatterns =[
    url(r'^testview', views.testview),
    #url(r'^createOrder/$', view=classviews.OrdersCreateView.as_view(), name='Printf_createorder'),
    url(r'^createOrder/(?P<merchant_id>[0-9]+)$', view=classviews.list, name='Printf_createorder'),
    url(r'^customerOrder/(?P<customer_id>[0-9]+)$', view=classviews.CustomersDetailView.as_view(), name='Printf_customerorder'),
    url(r'^customerOrder/$', view=classviews.CustomersDetailView.as_view(), name='Printf_customerorder'),
    url(r'^merchantList$', view=classviews.MerchantsListView.as_view(),name='Printf_merchantlist'),
    url(r'^merchantOrder/$', view=classviews.MerchantsDetailView.as_view(), name='Printf_merchantorder'),
    url(r'^updateOrder/(?P<order_id>[0-9]+)$',views.updateorder),
    url(r'^updateMerchant/$',views.updatemerchant),
    url(r'^updateMerchant/(?P<pk>[0-9]+)$',view=classviews.MerchantsUpdateView.as_view(),name='Printf_updatemerchant'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)