from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Stock
from .serializers import *
from api.yahoo import *
from django.http import JsonResponse
import re
from rest_framework.views import APIView


@api_view(['GET', 'POST'])
def stock_list(request):
    """
    List  products, or create a new product.
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        stocks = Stock.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(stocks, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = StockSerializer(data,context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/stocks/?page=' + str(nextPage), 'prevlink': '/api/stocks/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def stock_detail(request, ticker):
    """
    Retrieve, update or delete a product instance.
    """
    try:
        if re.compile(r'\w{1,4}').search(str(ticker)):
            stock = Stock.objects.get(ticker=ticker)
        else:
            stock = Stock.objects.get(pk=ticker)
    except Stock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StockSerializer(stock, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StockSerializer(stock, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def yahoo(request):

    data = {}

    #if request.query_params.get('function') == 'get_fixed_stock_value_list':
    data['result'] = get_fixed_stock_value_list('VOO', 30)
    return JsonResponse(data)

