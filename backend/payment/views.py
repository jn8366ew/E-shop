from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shipping.models import Shipping
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from product.models import Product
from coupons.models import FixedPriceCoupon, PercentageCoupon
from django.core.mail import send_mail
import braintree



gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=settings.BT_ENVIRONMENT,
        merchant_id=settings.BT_MERCHANT_ID,
        public_key=settings.BT_PUBLIC_KEY,
        private_key=settings.BT_PRIVATE_KEY
    )
)


class GenerateTokenView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            token = gateway.client_token.generate()
            return Response(
                {'braintree_token': token},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Error in GenerateTokenView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetPaymentTotalView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        # 부과세
        tax = 0.13

        shipping_id = request.query_params.get('shipping_id')
        shipping_id = str(shipping_id)

        coupon_name = request.query_params.get('coupon_name')
        coupon_name = str(coupon_name)

        try:
            cart = Cart.objects.get(user=user)

            # 특정 유저 카트에 아이템들이 있는지 확인한다.
            if not CartItem.objects.filter(cart=cart).exists():
                return Response(
                    {'error': 'Need to have items in cart'},
                    status=status.HTTP_404_NOT_FOUND
                )

            cart_items = CartItem.objects.filter(cart=cart)


            for cart_item in cart_items:
                if not Product.objects.filter(id=cart_item.product.id).exists():
                    return Response(
                        {'error': 'Product ID does not exist.'},
                        status=status.HTTP_404_NOT_FOUND
                    )


                if int(cart_item.count) > int(cart_item.product.quantity):
                    return Response(
                        {'error': 'Not enough items in stock'},
                        status=status.HTTP_200_OK
                    )


            # 총 주문 수량 계산
            total_amount = 0.0
            total_compare_amount = 0.0


            for cart_item in cart_items:
                total_amount += float(cart_item.product.price) * float(cart_item.count)
                total_compare_amount += float(cart_item.product.compare_price) * float(cart_item.count)

            total_compare_amount = round(total_compare_amount, 2)
            original_price = round(total_amount, 2)

            # 쿠폰 적용 후 가격을 위한 변수
            total_after_coupon = total_amount
            # 쿠폰 적용: 쿠폰 유효성 체크 -> 가격계산
            if coupon_name != '':

                # 가격고정쿠폰
                if FixedPriceCoupon.objects.filter(name__iexact=coupon_name).exists():
                    fixed_price_coupon = FixedPriceCoupon.objects.get(
                        name=coupon_name
                    )
                    discount_amount = float(fixed_price_coupon.discount_price)

                    if discount_amount < total_amount:
                        total_amount -= discount_amount
                        total_after_coupon = total_amount

                # 퍼센티지쿠폰
                elif PercentageCoupon.objects.filter(name__iexact=coupon_name).exists():
                    percentage_coupon = PercentageCoupon.objects.get(
                        name=coupon_name
                    )
                    discount_percentage = float(percentage_coupon.discount_percentage)

                    if discount_percentage > 1 and discount_percentage < 100:
                        total_amount -= (total_amount * (discount_percentage / 100))
                        total_after_coupon = total_amount

            # 쿠폰 적용후 총 가격 계산
            total_after_coupon = round(total_after_coupon, 2)


            # 부가가치세 계산
            estimated_tax = round(total_amount * tax, 2)

            # 부가가치세 + 총금액
            total_amount += (total_amount * tax)

            shipping_cost = 0.0

            # shipping_id가 유효한지 확인
            if Shipping.objects.filter(id__iexact=shipping_id).exists():
                shipping = Shipping.objects.get(id=shipping_id)
                shipping_cost = shipping.price
                total_amount += float(shipping_cost)

            # 실제 총 수량
            total_amount = round(total_amount, 2)

            return Response(
                {
                    'original_price': f'{original_price:.2f}',
                    'total_after_coupon': f'{total_after_coupon:.2f}',
                    'total_amount': f'{total_amount:.2f}',
                    'total_compare_amount': f'{total_compare_amount:.2f}',
                    'estimated_tax': f'{estimated_tax:.2f}',
                    'shipping_cost': f'{shipping_cost:.2f}'
                 },
                 status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Error in GetPaymentTotalView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProcessPaymentView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        print(data['coupon_name'])

        tax = 0.13

        nonce = data['nonce']
        shipping_id = str(data['shipping_id'])
        coupon_name = str(data['coupon_name'])
        print('coupon_name', coupon_name)
        full_name = data['full_name']
        address_line_1 = data['address_line_1']
        address_line_2 = data['address_line_2']
        city = data['city']
        state_province_region = data['state_province_region']
        postal_zip_code = data['postal_zip_code']
        country_region = data['country_region']
        telephone_number = data['telephone_number']

        if not Shipping.objects.filter(id__iexact=shipping_id).exists():
            print("Invalid shipping option at shipping.objects.filter")
            return Response(
                {'error': 'Invalid shipping option at shipping.objects.filter'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = Cart.objects.get(user=user)

        # 특정 유저 카트에 아이템들이 있는지 확인한다.
        if not CartItem.objects.filter(cart=cart).exists():
            print("Invalid shipping option at CartItem.objects.filter")
            return Response(
                {'error': 'Need to have items in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = CartItem.objects.filter(cart=cart)

        # 카트에 있는 상품 id가 유효한지 확인
        for cart_item in cart_items:
            if not Product.objects.filter(id=cart_item.product.id).exists():
                print("A product_id does not exist")
                return Response(
                    {'error': 'A product_id does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if int(cart_item.count) > int(cart_item.product.quantity):
                return Response(
                    {'error': 'Not enough items in stock'},
                    status=status.HTTP_200_OK
                )

        # 총 주문 수량 계산
        total_amount = 0.0

        for cart_item in cart_items:
            total_amount += float(cart_item.product.price) * float(cart_item.count)

        # 쿠폰가격 적용하기
        if coupon_name != '':
            # 가격고정쿠폰
            if FixedPriceCoupon.objects.filter(name__iexact=coupon_name).exists():
                fixed_price_coupon = FixedPriceCoupon.objects.get(
                    name=coupon_name
                )
                discount_amount = float(fixed_price_coupon.discount_price)

                if discount_amount < total_amount:
                    total_amount -= discount_amount
                print('FixedPriceCoupon Applied: ', total_amount)

            # 퍼센티지쿠폰
            elif PercentageCoupon.objects.filter(name__iexact=coupon_name).exists():
                percentage_coupon = PercentageCoupon.objects.get(
                    name=coupon_name
                )
                discount_percentage = float(percentage_coupon.discount_percentage)

                if discount_percentage > 1 and discount_percentage < 100:
                    total_amount -= (total_amount * (discount_percentage / 100))
                print('PercentageCoupon Applied: ', total_amount)



        # 부가가치세 + 총금액
        total_amount += float(total_amount * tax)


        shipping = Shipping.objects.get(id=int(shipping_id))

        shipping_name = shipping.name
        shipping_time = shipping.time_to_delivery
        shipping_price = shipping.price

        # 실제 총 수량
        total_amount += float(shipping_price)
        total_amount = round(total_amount, 2)
        print('Final Check:', total_amount)
        # 거래(Transaction) 생성
        try:
            newTransaction = gateway.transaction.sale(
                {
                    'amount': str(total_amount),
                    'payment_method_nonce': str(nonce['nonce']),
                    'options': {
                        'submit_for_settlement': True
                    }
                }
            )
        except:
            return Response(
                {'error': 'Error in ProcessPaymentView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 거래 성공시 상품의 오브젝트(수량, 판매량) 업데이트
        if newTransaction.is_success and newTransaction.transaction:
            for cart_item in cart_items:
                # 상품 오브젝트를 가져와서 갱신
                update_product = Product.objects.get(id=cart_item.product.id)

                # 위의 오브젝트의 수량을 계산
                quantity = int(update_product.quantity) - int(cart_item.count)

                # 판매량 계산
                sold = int(update_product.sold) + int(cart_item.count)

                # 상품 오브젝트의 데이터를 갱신
                Product.objects.filter(id=cart_item.product.id).update(
                    quantity=quantity, sold=sold
                )

            try:
                order = Order.objects.create(
                    user=user,
                    transaction_id= newTransaction.transaction.id,
                    amount= total_amount,
                    full_name=full_name,
                    address_line_1 = address_line_1,
                    address_line_2 = address_line_2,
                    city = city,
                    state_province_region = state_province_region,
                    postal_zip_code = postal_zip_code,
                    country_region = country_region,
                    telephone_number = telephone_number,
                    shipping_name = shipping_name,
                    shipping_time = shipping_time,
                    shipping_price = float(shipping_price)
                )
            except:
                return Response(
                    {'error': 'Transaction succeeded, but failed to create the order.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            for cart_item in cart_items:
                try:
                    product = Product.objects.get(id=cart_item.product.id)

                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        name=product.name,
                        price=cart_item.product.price,
                        count=cart_item.count
                    )
                except:
                    return Response(
                        {'error': 'Transaction succeeded and order created, but failed to create an OrderItem object.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            # 주문서를 주문한 User의 메일로 보낸다
            try:
                send_mail(
                    'Your Order Details',
                    'Dear ' + full_name + ',\n\n' +
                    'We received your order.\n' +
                    'We are processing your order. Thank you.\n' +
                    'Sincerely,\n' +
                    'Shop',
                    'ilsanmwfshop@gmail.com',
                    [user.email],
                    fail_silently=False
                )
            except:
                return Response(
                    {'error': 'Transaction succeeded and order created, but failed to sending an email.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                CartItem.objects.filter(cart=cart).delete()

                Cart.objects.filter(user=user).update(total_items=0)
            except:
                return Response(
                    {'error': 'Transaction succeeded, order created, and sent email but failed to clear an Cart.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {'success': 'All transaction processes completed.'},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {'error': 'Transaction Failed'},
                status=status.HTTP_400_BAD_REQUEST
            )