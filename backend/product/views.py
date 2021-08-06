from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Product
from .serializers import ProductSerializer
from category.models import Category
from django.db.models import Q







class ReadProductView(APIView):
    """
    하나의 상품 오브젝트를 읽는 기능
    url: api/products/product/<productId>
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id = int(productId)
        except:
            return Response({'error': 'Product ID must be an integer'}, status=status.HTTP_404_NOT_FOUND)

        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)

            product = ProductSerializer(product)


            return Response({'product': product.data},
                            status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Product with this id does not exist'},
                            status=status.HTTP_404_NOT_FOUND)



class ListProductsView(APIView):
    """
    복수의 상품 오브젝트를 읽어서 나열하는 기능, query parameter 사용
    url: api/products/get-products

    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        sort_by = request.query_params.get('sortBy')
        if not (sort_by == 'date_created' or sort_by == 'price' or
                sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_created'

        order = request.query_params.get('order')
        limit = request.query_params.get('limit')

        if not limit:
            limit = 6

        try:
            limit = int(limit)
        except:
            return Response({'error': 'Limit must be an integer'},
                            status=status.HTTP_404_NOT_FOUND)

        if limit <= 0:
            limit = 6


        # order의 값이 'desc'일 경우 내림차순으로 정렬
        if order == 'desc':
            sort_by = '-' + sort_by
            products = Product.objects.order_by(sort_by).all()[:int(limit)]
        elif order == 'asc':
            products = Product.objects.order_by(sort_by).all()[:int(limit)]
        else:
            products = Product.objects.order_by(sort_by).all()


        products = ProductSerializer(products, many=True)

        if products:
            return Response({'products': products.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No products to list'},
                            status=status.HTTP_404_NOT_FOUND)


class ListSearchView(APIView):
    """
    입력된 문자열을 바탕으로 product 오브젝트를 가져와서 나열하는 기능
    url: api/products/search
    포스트 방식을 이용한 이유:
    1. 서버에 데이터(검색어)를 보내고 다시 불러들인다.
    2. 다른 유저가 querystring을 보길 원치 않는다.
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except:
            return Response({'error': 'category_id must be an integer'},
                            status=status.HTTP_404_NOT_FOUND)
        search = data['search']

        # 검색 필드 체크
        if len(search) == 0:
            # 검색 조건이 없다면 모든 제품 가져오기
            search_results = Product.objects.order_by('-date_created').all()
        else:
            # 검색 조건이 존재하다면, search data에 포함된 이름도 같이 description에 의해 필터링한다
            search_results = Product.objects.filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )

        # 카테고리 전부 가져오기
        if category_id == 0:
            search_results = ProductSerializer(search_results, many=True)
            return Response({'search_products': search_results.data},
                             status=status.HTTP_200_OK)

        # 카테고리 id가 없을 때
        if not Category.objects.filter(id=category_id).exists():
            return Response({'Error': 'Category not found.'},
                            status=status.HTTP_404_NOT_FOUND)


        category = Category.objects.get(id=category_id)

        # category에 부모가 있을 때, 상품 오브젝트 정렬 -> 이 카테고리만 필터링한다.
        if category.parent:
            search_results = search_results.order_by(
                '-date_created'
            ).filter(category=category)

        # 부모 카테고리가 없을 때
        else:
            # 부모가 없고 자식도 아닌 카테고리일경우 -> 상품 오브젝트 정렬 -> 이 카테고리만 필터링한다.
            if not Category.objects.filter(parent=category).exists():
                search_results = search_results.order_by(
                    '-date_created'
                ).filter(category=category)

            # 부모가 없고 자식 카테고리 있을경우 하위 카테고리도 포함시킨다. (루트 카테고리)
            else:
                categories = Category.objects.filter(parent=category)
                filtered_categories = [category]

                for cat in categories:
                    filtered_categories.append(cat)

                # 필터된 카테고리가 변경되지 않도록 튜플로 형변환
                filtered_categories = tuple(filtered_categories)
                search_results = search_results.order_by(
                    '-date_created'
                ).filter(category__in=filtered_categories)

        search_results = ProductSerializer(search_results, many=True)
        return Response({'search_products': search_results.data},
                        status=status.HTTP_200_OK)




class ListRelatedView(APIView):
    """
    productId가 가진 category를 바탕으로 오브젝트(들)를 나열. 자기자신은 제외
    url: api/products/related/<productId>
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id = int(productId)
        except:
            return Response({'error': 'Product ID must be an integer'},
                            status=status.HTTP_404_NOT_FOUND)


        # 이 아이디를 가진 상품이 없을 경우
        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': 'Product with this product ID does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        category = Product.objects.get(id=product_id).category

        if Product.objects.filter(category=category).exists():
            # 카테고리에 부모가 있을경우 이 카테고리에만 필터 적용
            if category.parent:
                related_products = Product.objects.order_by(
                    '-sold'
                ).filter(category=category)
            else:
                # 부모가 없고 자식도 아닌 카테고리일경우
                if not Category.objects.filter(parent=category).exists():
                    related_products = Product.objects.order_by(
                        '-sold'
                    ).filter(category=category)

                # 부모가 없고 자식 카테고리가 있을경우 자기 자신과 서브 카테고리 출력 (루트 카테고리)
                else:
                    categories = Category.objects.filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    related_products = Product.objects.order_by(
                        '-sold'
                    ).filter(category__in=filtered_categories)

            # 중요: 연관된 상품을 찾기 위해 우리가 보고 있는 상품 id는 배제한다.
            related_products = related_products.exclude(id=product_id)
            related_products = ProductSerializer(related_products, many=True)

            if len(related_products.data) > 3:
                return Response({'related_products': related_products.data[:3]},
                                status=status.HTTP_200_OK)

            elif len(related_products.data) > 0:
                return Response({'related_products': related_products.data},
                                status=status.HTTP_200_OK)

            else:
                return Response({'alert': 'No related products found'},
                                status=status.HTTP_200_OK)

        else:
            return Response({'alert': 'No related products found'},
                            status=status.HTTP_200_OK)



class ListBySearchView(APIView):
    """
    만든 날짜/가격/판매순/이름 바탕으로 검색 후 상품 오브젝트를 나열
    url: api/products/by/search
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        try:
            category_id = int(data['category_id'])
        except:
            return Response({'error': 'category_id must be an integer.'},
                            status=status.HTTP_404_NOT_FOUND)
        price_range = data['price_range']
        sort_by = data['sort_by']

        if not (sort_by == 'date_created' or sort_by == 'price' or
                sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_created'

        if not sort_by:
            sort_by = 'date_created'

        order = data['order']

        # 카테고리 id = 0 -> 모든 카테고리
        if category_id == 0:
            product_results = Product.objects.all()

        elif not Category.objects.filter(id=category_id).exists():
            return Response({'error': 'This category does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            category = Category.objects.get(id=category_id)
            # 카테고리에 부모가 있을경우 이 카테고리에만 필터 적용
            if category.parent:
                product_results = Product.objects.filter(category=category)
            else:
                # 이 카테고리에 자식 카테고리가 없을 때 이 카테고리 자체를 필터링
                if not Category.objects.filter(parent=category).exists():
                    product_results = Product.objects.filter(category=category)

                # 이 부모 카테고리에 자식 카테고리 있을경우 두 카테고리를 필터
                else:
                    categories = Category.objects.filter(parent=category)
                    filtered_categories = [category]

                    for cat in categories:
                        filtered_categories.append(cat)

                    filtered_categories = tuple(filtered_categories)
                    product_results = Product.objects.filter(
                        category__in=filtered_categories)

        # 가격 대로 필터링
        if price_range == '1 - 19':
            product_results = product_results.filter(price__gte=1)
            product_results = product_results.filter(price__lt=19)
        elif price_range == '20 - 39':
            product_results = product_results.filter(price__gte=20)
            product_results = product_results.filter(price__lt=39)
        elif price_range == '40 - 59':
            product_results = product_results.filter(price__gte=40)
            product_results = product_results.filter(price__lt=59)
        elif price_range == '60 - 79':
            product_results = product_results.filter(price__gte=60)
            product_results = product_results.filter(price__lt=79)
        elif price_range == 'More than 80':
            product_results = product_results.filter(price__gte=80)

        # order와 sort_by에 의한 정렬(내림 // 올림차순)
        if order == 'desc':
            sort_by = '-' + sort_by
            product_results = product_results.order_by(sort_by)
        elif order == 'asc':
            product_results = product_results.order_by(sort_by)
        else:
            product_results = product_results.order_by(sort_by)

        product_results = ProductSerializer(product_results, many=True)

        if len(product_results.data) > 0:
            return Response({'filtered_products': product_results.data},
                            status=status.HTTP_200_OK)

        else:
            return Response({'alert': 'No product found'},
                            status=status.HTTP_200_OK)






