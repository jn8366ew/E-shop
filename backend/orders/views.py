from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem

class ListOrdersView(APIView):
    """
    JSON 데이터 형식
    {
        orders: [
                    {
                        status: "",
                        transaction_id: "",
                        ...
                    }
                ]
    }
    """
    def get(self, request, format=None):
        user = self.request.user

        try:
            # user의 order 오브젝트를 받고 날짜에 따라 정렬한다.
            orders = Order.objects.order_by('-date_issued').filter(user=user)

            # 프론트엔드에 보낼 order 오브젝트 데이터를 이곳에 저장
            result = []

            for order in orders:
                item = {}
                item['status'] = order.status
                item['transaction_id'] = order.transaction_id
                item['amount'] = order.amount
                item['date_issued'] = order.date_issued

                result.append(item)

            return Response({'orders': result}, status=status.HTTP_200_OK)

        except:
            return Response({'error: error at ListOrdersView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 단일 order 오브젝트를 처리하는 view
class ListOrderDetailView(APIView):
    """
    JSON 데이터 형식
    {
        order: {
                status="",
                transaction_id: "",
                order_items: [
                    {
                        name: "",
                        price: "",
                        count: "",
                    },

                ]
    }
    """
    def get(self, request, transactionId, format=None):
        user = self.request.user


        try:
            # user와 transaction_id가 있는지 확인한다.
            if Order.objects.filter(user=user, transaction_id=transactionId).exists():
                order = Order.objects.get(user=user, transaction_id=transactionId)

                # 프론트엔드에 보낼 order 오브젝트 데이터를 이곳에 저장
                result = {}


                result['status'] = order.status
                result['transaction_id'] = order.transaction_id
                result['amount'] = order.amount
                result['date_issued'] = order.date_issued
                result['full_name'] = order.full_name
                result['address_line_1'] = order.address_line_1
                result['address_line_2'] = order.address_line_2
                result['city'] = order.city
                result['state_province_region'] = order.state_province_region
                result['postal_zip_code'] = order.postal_zip_code
                result['country_region'] = order.country_region
                result['telephone_number'] = order.telephone_number
                result['shipping_name'] = order.shipping_name
                result['shipping_time'] = order.shipping_time
                result['shipping_price'] = order.shipping_price
                result['date_issued'] = order.date_issued

                order_items = OrderItem.objects.order_by('-date_added').filter(order=order)

                # Order 오브젝트와 관련된 order_items객체
                result['order_items'] = []
                for order_item in order_items:
                    sub_item = {}

                    sub_item['name'] = order_item.name
                    sub_item['price'] = order_item.price
                    sub_item['count'] = order_item.count

                    result['order_items'].append(sub_item)



                return Response({'order': result}, status=status.HTTP_200_OK)

            else:
                return Response(
                    {'error': 'Transaction_id with this order does not exist'},
                    status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'error: error at ListOrderDetailView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


