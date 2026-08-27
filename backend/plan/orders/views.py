from django.shortcuts import render

from rest_framework import viewsets, status
from .models import Orders
from .serializers import OrdersSerializer

from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import HttpResponse

from django_daraja.mpesa.core import MpesaClient

# Create your views here.

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    @action(detail=True, methods=['get'], url_path='payment-methods')
    def get_payment_methods(self, request, pk=None):
        order = self.get_object()
        payment_methods = order.payments_set.all()
        serializer = PaymentsSerializer(payment_methods, many=True)
        return Response(serializer.data)
    





def index(request):
     cl = MpesaClient()
     phone_number = '0714531306'
     amount = 1
     account_reference = 'reference'
     transaction_desc = 'Description'
     callback_url = 'https://api.darajambili.com/express-payment'
     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
     return HttpResponse(response)


