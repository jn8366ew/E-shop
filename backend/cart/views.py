from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from product.models import Product
from product.serializers import ProductSerializer


class GetItemView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.order_by('product').filter(cart=cart)

            result = []

            # 카트에 있는 카트 상품이 있는지 확인하고, 있을시시 시리얼라이징하여 rsponse 한다.
            if CartItem.objects.filter(cart=cart).exists():
                for cart_item in cart_items:
                    #
                    # {
                    #   'id' : '1',
                    #   'count': '3',
                    #   'product': {
                    #       'id':1
                    # }}

                    item = {}
                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = Product.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)
                    item['product'] = product.data

                    result.append(item)
                return Response({'cart': result},
                                status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Exception in GetItemView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddItemView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])

        except:
            return Response({'error': 'Product_id must be integer'},
                            status=status.HTTP_404_NOT_FOUND)

        count = 1

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': ' The product does not exists'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)

            cart = Cart.objects.get(user=user)


            # 카트에 상품 제품이 이미 추가 되어 있을 경우
            if CartItem.objects.filter(cart=cart, product=product).exists():
                return Response({'error': 'Item already in cart'},
                                status=status.HTTP_409_CONFLICT)


            # 카트에 특정 상품의 수가 0이 아닐경우 CartItem의 오브젝트를 만든다.
            if int(product.quantity) > 0:
                CartItem.objects.create(
                    product=product, cart=cart, count=count
                )

                # 카트에 있는 모든 상품이 추가되었는지를 확인한다.
                if CartItem.objects.filter(cart=cart, product=product).exists():
                    # 카트에 있는 모든 제품의 수를 합한다.
                    total_items = int(cart.total_items) + 1
                    Cart.objects.filter(user=user).update(
                        total_items=total_items
                    )


                cart_items = CartItem.objects.order_by('product').filter(cart=cart)

                result = []

                for cart_item in cart_items:

                    item = {}
                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = Product.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)
                    item['product'] = product.data

                    result.append(item)

                # DB에 오브젝트를 생성했기 때문에 201으로 Response
                return Response({'cart': result},
                                status=status.HTTP_201_CREATED)

            else:
                return Response({'alert': 'Not enough of this item in stock'},
                                status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Exception in AddItemView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTotalView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)

            total_cost = 0.0
            total_compare_cost = 0.0

            if cart_items.exists():
                for cart_item in cart_items:
                    total_cost += float(cart_item.product.price) * float(cart_item.count)
                    total_compare_cost += float(cart_item.product.compare_price) * float(cart_item.count)

                    total_cost = round(total_cost, 2)
                    total_compare_cost = round(total_compare_cost, 2)

            return Response({'total_cost': total_cost,
                             'total_compare_cost': total_compare_cost},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Exception in GetTotalView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTotalItemView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
            total_items = cart.total_items

            return Response({'total_items': total_items},
                            status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Exception in GetTotalItemView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateItemView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])

        except:
            return Response({'error': 'Product_id must be integer'},
                            status=status.HTTP_404_NOT_FOUND)


        # count가 int형으로 parsing 되지 않음을 방지하기 위해 try/except 사용
        try:
            count = int(data['count'])
        except:
            return Response({'error': 'Count value must be integer'},
                            status=status.HTTP_404_NOT_FOUND)


        # 상품 오브젝트가 있는가를 확인
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': ' The product does not exists'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)

            cart = Cart.objects.get(user=user)

            # 카트에 상품이 없을경우
            if not CartItem.objects.filter(cart=cart, product=product).exists():
                return Response({'error': 'This product is not in your cart'},
                                status=status.HTTP_404_NOT_FOUND)


            quantity = product.quantity

            # 유저가 구입할 제품의 양(count)이 상품이 남아 있는 수보다 같거나 적을때
            # 카트아이템 오브젝트 갱신.
            if count <= quantity:
                CartItem.objects.filter(
                    product=product, cart=cart
                ).update(count=count)

                cart_items = CartItem.objects.order_by('product').filter(cart=cart)

                result = []

                for cart_item in cart_items:
                    item = {}
                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = Product.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)
                    item['product'] = product.data

                    result.append(item)

                # DB에 오브젝트를 '갱신'했기 때문에 200으로 Response
                return Response({'cart': result},
                                status=status.HTTP_200_OK)

            else:
                return Response({'alert': 'Not enough of this item in stock'},
                                status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Exception in UpdateItemView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveItemView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(data['product_id'])

        except:
            return Response({'error': 'Product_id must be integer'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': ' The product does not exists'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get(user=user)

            # 카트에 상품이 없을경우
            if not CartItem.objects.filter(cart=cart, product=product).exists():
                return Response({'error': 'This product is not in your cart.'},
                                status=status.HTTP_404_NOT_FOUND)

            # 카트에 있는 아이템을 삭제한다.
            CartItem.objects.filter(cart=cart, product=product).delete()

            # 삭제 성공후 오브젝트가 남아 있을 경우 카트아이템의 total_item 값을 갱신.
            if not CartItem.objects.filter(cart=cart, product=product).exists():
                total_items = int(cart.total_items) - 1
                Cart.objects.filter(user=user).update(total_items=total_items)

            result = []
            cart_items = CartItem.objects.order_by('product').filter(cart=cart)

            # 카트아이템 삭제후 오브젝트가 남아있을 경우 재갱신한다.
            if CartItem.objects.filter(cart=cart).exists():
                for cart_item in cart_items:
                    item = {}
                    item['id'] = cart_item.id
                    item['count'] = cart_item.count
                    product = Product.objects.get(id=cart_item.product.id)
                    product = ProductSerializer(product)
                    item['product'] = product.data

                    result.append(item)

            # DB에 오브젝트를 '갱신'했기 때문에 200으로 Response
            return Response({'cart': result},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Exception in RemoveItemView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmptyCartView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)

            # 카트에 오브젝트가 있는지 확인한다.
            if not CartItem.objects.filter(cart=cart).exists():
                return Response({'success': 'Cart is already empty'},
                                status=status.HTTP_200_OK)

            # 전부 삭제.
            CartItem.objects.filter(cart=cart).delete()

            # Update cart to have no item
            Cart.objects.filter(user=user).update(total_items=0)
            return Response({'success': 'Cart emptied successfully.'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Exception in EmptyCartView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SyncCartView(APIView):
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            cart_items = data['cart_items']

            for cart_item in cart_items:
                cart = Cart.objects.get(user=user)
                try:
                    product_id = int(cart_item['product_id'])
                except:
                    return Response({'error': 'Product_id must be integer'},
                                    status=status.HTTP_404_NOT_FOUND)


                if not Product.objects.filter(id=product_id).exists():
                    return Response({'error': 'The product with this id does not exist.'},
                                    status=status.HTTP_404_NOT_FOUND)

                # 싱크 시작
                product = Product.objects.get(id=product_id)
                quantity = product.quantity

                # 카트 싱크에 관련된 상황들 

                if CartItem.objects.filter(cart=cart, product=product).exists():
                    # local 카트를 유저에 카트에 업데이트 한다. 

                    item = CartItem.objects.get(cart=cart, product=product)
                    count = item.count

                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1

                    # (로컬 카트에 있는 상품 수량) + (DB에 있는 카트의 아이템 수량)이 상품 수량보다 같거나 적을경우
                    # 로컬카트상품수량 + DB카트상품수량을 그대로 합한다.
                    if (cart_item_count + int(count)) <= int(quantity):
                        updated_count = cart_item_count + int(count)
                        CartItem.objects.filter(
                            cart=cart, product=product).update(count=updated_count)


                else:
                    # local 카트를 유저에 카트에 추가 한다.
                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1

                    if cart_item_count <= quantity:
                        CartItem.objects.create(
                            product=product,
                            cart=cart,
                            count=cart_item_count
                        )

                    # 카트아이템에 오브젝트 존재 할 시 총 수량 갱신
                        if CartItem.objects.filter(cart=cart, product=product).exists():
                            total_items = int(cart.total_items) + 1
                            Cart.objects.filter(user=user).update(
                                total_items=total_items
                            )

            return Response(
                {'success': 'Cart Synchronized'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response({'error': 'Exception in SyncCartView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

