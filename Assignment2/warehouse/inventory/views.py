from rest_framework import viewsets
from .models import Item, Purchase, PurchaseDetail, Sell, SellDetail
from .serializers import ItemSerializer, PurchaseSerializer, PurchaseDetailSerializer, SellSerializer, SellDetailSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework import status

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.filter(is_deleted=False)
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            purchase = serializer.save()
            # add purchase details if any
            purchase_details = request.data.get('purchase_details', [])
            for detail in purchase_details:
                PurchaseDetail.objects.create(
                    item_code=Item.objects.get(code=detail['item_code']),
                    quantity=detail['quantity'],
                    unit_price=detail['unit_price'],
                    header_code=purchase
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellViewSet(viewsets.ModelViewSet):
    queryset = Sell.objects.filter(is_deleted=False)
    serializer_class = SellSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sell = serializer.save()
            # Add sales details if any
            sell_details = request.data.get('sell_details', [])
            for detail in sell_details:
                SellDetail.objects.create(
                    item_code=Item.objects.get(code=detail['item_code']),
                    quantity=detail['quantity'],
                    header_code=sell
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(APIView):
    def get(self, request):
        items = Item.objects.filter(is_deleted=False)  # Retrieve all items that are not deleted
        serializer = ItemSerializer(items, many=True)

        # Arrange the data according to the desired format
        response_data = {
            "items": [],
            "item_code": serializer.data[0]["code"] if serializer.data else None,
            "name": serializer.data[0]["name"] if serializer.data else None,
            "unit": serializer.data[0]["unit"] if serializer.data else None,
            "summary": {
                "in_qty": 0,
                "out_qty": 0,
                "balance_qty": 0,
                "balance": 0,
            }
        }

        # Calculate total in_qty, out_qty, balance_qty, and balance
        for item in serializer.data:
            # Get purchase and sale details for this item
            purchases = PurchaseDetail.objects.filter(item_code=item['id'])
            sales = SellDetail.objects.filter(item_code=item['id'])

            in_qty = sum(purchase.quantity for purchase in purchases)
            out_qty = sum(sale.quantity for sale in sales)

            # Add items to response_data
            response_data["items"].append({
                "date": item.get("created_at"),  # Add create date
                "description": item.get("description", "No description"),  # get descriptions
                "code": item["code"],
                "in_qty": in_qty,
                "in_price": item.get("balance", 0),  # get balance
                "in_total": in_qty * item.get("balance", 0),  # count total
                "out_qty": out_qty,
                "out_price": 0,  
                "out_total": 0,  
                "stock_qty": [in_qty],  # get stock count
                "stock_price": [item.get("balance", 0)],  # get balance
                "stock_total": [in_qty * item.get("balance", 0)],  # total count
                "balance_qty": item.get("stock", 0),  # get stock count
                "balance": item.get("balance", 0),  # get balance
            })

            # Update summary
            response_data["summary"]["in_qty"] += in_qty
            response_data["summary"]["out_qty"] += out_qty
            response_data["summary"]["balance_qty"] += item.get("stock", 0)
            response_data["summary"]["balance"] += item.get("balance", 0) * item.get("stock", 0)

        return Response({"result": response_data}, status=status.HTTP_200_OK)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_deleted=False)
    serializer_class = ItemSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.filter(is_deleted=False)
    serializer_class = PurchaseSerializer

class PurchaseDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseDetail.objects.all()
    serializer_class = PurchaseDetailSerializer

class SellViewSet(viewsets.ModelViewSet):
    queryset = Sell.objects.filter(is_deleted=False)
    serializer_class = SellSerializer

class SellDetailViewSet(viewsets.ModelViewSet):
    queryset = SellDetail.objects.all()
    serializer_class = SellDetailSerializer

@api_view(['GET'])
def stock_report(request, item_code):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Retrieving items by item_code
    item = Item.objects.filter(code=item_code).first()
    if not item:
        return Response({"error": "Item not found"}, status=404)

    # Retrieving purchase details within a date range
    purchases = PurchaseDetail.objects.filter(
        item_code=item,
        header_code__date__range=[start_date, end_date]
    ).values('header_code__date', 'header_code__description', 'header_code__code', 'quantity', 'unit_price')

    # Retrieving sales details within a date range
    sales = SellDetail.objects.filter(
        item_code=item,
        header_code__date__range=[start_date, end_date]
    ).values('header_code__date', 'header_code__description', 'header_code__code', 'quantity')

    report_data = {
        "items": [],
        "item_code": item.code,
        "name": item.name,
        "unit": item.unit,
        "summary": {
            "in_qty": 0,
            "out_qty": 0,
            "balance_qty": item.stock,
            "balance": item.balance,
        }
    }

    # Calculating purchase report
    stock_qty = []
    stock_price = []
    stock_total = []
    
    for purchase in purchases:
        in_qty = purchase['quantity']
        in_price = purchase['unit_price']
        in_total = in_qty * in_price
        report_data["items"].append({
            "date": purchase['header_code__date'].strftime("%d-%m-%Y"),
            "description": purchase['header_code__description'],
            "code": purchase['header_code__code'],
            "in_qty": in_qty,
            "in_price": in_price,
            "in_total": in_total,
            "out_qty": 0,
            "out_price": 0,
            "out_total": 0,
            "stock_qty": [in_qty],
            "stock_price": [in_price],
            "stock_total": [in_total],
            "balance_qty": report_data["summary"]["balance_qty"] + in_qty,
            "balance": report_data["summary"]["balance"] + in_total,
        })
        report_data["summary"]["in_qty"] += in_qty
        report_data["summary"]["balance_qty"] += in_qty
        report_data["summary"]["balance"] += in_total

        # Save data for stock
        stock_qty.append(in_qty)
        stock_price.append(in_price)
        stock_total.append(in_total)

    # Calculating sales reports
    for sale in sales:
        out_qty = sale['quantity']
        report_data["items"].append({
            "date": sale['header_code__date'].strftime("%d-%m-%Y"),
            "description": sale['header_code__description'],
            "code": sale['header_code__code'],
            "in_qty": 0,
            "in_price": 0,
            "in_total": 0,
            "out_qty": out_qty,
            "out_price": 0,  
            "out_total": 0, 
            "stock_qty": [0],
            "stock_price": [0],
            "stock_total": [0],
            "balance_qty": report_data["summary"]["balance_qty"] - out_qty,
            "balance": report_data["summary"]["balance"],  # Update balance 
        })
        report_data["summary"]["out_qty"] += out_qty
        report_data["summary"]["balance_qty"] -= out_qty

    # Retrieving data stock to report
    report_data["items"][-1]["stock_qty"] = stock_qty
    report_data["items"][-1]["stock_price"] = stock_price
    report_data["items"][-1]["stock_total"] = stock_total

    return Response({"result": report_data})

@api_view(['GET'])
def stock_report(request, item_code):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Retrieving items by item_code
    item = Item.objects.filter(code=item_code).first()
    if not item:
        return Response({"error": "Item not found"}, status=404)

    # Retrieving purchase details within a date range
    purchases = PurchaseDetail.objects.filter(
        item_code=item,
        header_code__date__range=[start_date, end_date]
    ).values('header_code__date', 'header_code__description', 'header_code__code', 'quantity', 'unit_price')

    # Retrieving sales details within a date range
    sales = SellDetail.objects.filter(
        item_code=item,
        header_code__date__range=[start_date, end_date]
    ).values('header_code__date', 'header_code__description', 'header_code__code', 'quantity')

    report_data = {
        "items": [],
        "item_code": item.code,
        "name": item.name,
        "unit": item.unit,
        "summary": {
            "in_qty": 0,
            "out_qty": 0,
            "balance_qty": item.stock,
            "balance": item.balance,
        }
    }

    # Retrieving purchase 
    for purchase in purchases:
        in_qty = purchase['quantity']
        in_price = purchase['unit_price']
        in_total = in_qty * in_price
        report_data["items"].append({
            "date": purchase['header_code__date'].strftime("%d-%m-%Y"),
            "description": purchase['header_code__description'],
            "code": purchase['header_code__code'],
            "in_qty": in_qty,
            "in_price": in_price,
            "in_total": in_total,
            "out_qty": 0,
            "out_price": 0,
            "out_total": 0,
            "balance_qty": report_data["summary"]["balance_qty"] + in_qty,
            "balance": report_data["summary"]["balance"] + in_total,
        })
        report_data["summary"]["in_qty"] += in_qty
        report_data["summary"]["balance_qty"] += in_qty
        report_data["summary"]["balance"] += in_total

    # Retrieving sell count
    for sale in sales:
        out_qty = sale['quantity']
        report_data["items"].append({
            "date": sale['header_code__date'].strftime("%d-%m-%Y"),
            "description": sale['header_code__description'],
            "code": sale['header_code__code'],
            "in_qty": 0,
            "in_price": 0,
            "in_total": 0,
            "out_qty": out_qty,
            "out_price": 0,
            "out_total": 0,
            "balance_qty": report_data["summary"]["balance_qty"] - out_qty,
            "balance": report_data["summary"]["balance"],
        })
        report_data["summary"]["out_qty"] += out_qty
        report_data["summary"]["balance_qty"] -= out_qty

    return Response({"result": report_data})