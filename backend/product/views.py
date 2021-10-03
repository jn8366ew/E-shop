from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Product
from .serializers import ProductSerializer
from category.models import Category
from django.db.models import Q

from .filter_funcs import filter_by_category



class ReadProductView(APIView):
    """
    A view to retrieve a single product for any user
    url: api/products/product/<productId>
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        # check productId whether integer or not
        try:
            product_id = int(productId)
        except:
            return Response({'error': 'Product ID must be an integer'},
                            status=status.HTTP_404_NOT_FOUNDr)


        # check a product associated with product_id whether exists
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
    A view to retrieve multiple products for any user
    url: api/products/get-products?order=<>&sortBy=<>?limit=<>
    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        sort_by = request.query_params.get('sortBy')
        if not (sort_by == 'date_created' or sort_by == 'price' or
                sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_created'

        if not sort_by:
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
    A view retrieve products by category_id and search keyword
    url: api/products/search
    requests: (int)category_id, (str)search
    """

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        # retrieve requested JSON data from client
        data = self.request.data

        try:
            category_id = int(data['category_id'])
        except:
            return Response({'error': 'category_id must be an integer'},
                            status=status.HTTP_404_NOT_FOUND)
        search = data['search']

        # check search keyword
        # if no keyword, retrieve all products.
        if len(search) == 0:
            search_results = Product.objects.order_by('-date_created').all()
        else:
            # retrieve products associated with description or name
            search_results = Product.objects.filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )

        # if category_id is 0, retrieve all products.
        if category_id == 0:
            search_results = ProductSerializer(search_results, many=True)
            return Response({'search_products': search_results.data},
                             status=status.HTTP_200_OK)


        # check category id whether exists.
        if not Category.objects.filter(id=category_id).exists():
            return Response({'Error': 'Category not found.'},
                            status=status.HTTP_404_NOT_FOUND)


        category = Category.objects.get(id=category_id)

        # Refactored statements (Oct/3/2021)
        search_results = filter_by_category(category, search_results)
        search_results = search_results.order_by('-date_created')


        # setting a nested serializer as we might have mutiple products
        search_results = ProductSerializer(search_results, many=True)
        print(search_results)
        return Response({'search_products': search_results.data},
                        status=status.HTTP_200_OK)




def filter_by_category(category, previous_results=None):
    # If category has a parent, filter only by this category and not the parent as well
    if category.parent:
        if previous_results:
            return previous_results.filter(category=category)
        else:
            return Product.objects.filter(category=category)
    else:
        # If this parent category does not have any children categories
        # then just filter by the category itself
        if not Category.objects.filter(parent=category).exists():
            if previous_results:
                return previous_results.filter(category=category)
            else:
                return Product.objects.filter(category=category)
        # If this parent category has children, filter by both the parent category and it's children
        else:
            categories = Category.objects.filter(parent=category)
            filtered_categories = [category]

            for cat in categories:
                filtered_categories.append(cat)

            filtered_categories = tuple(filtered_categories)
            if previous_results:
                return previous_results.filter(category__in=filtered_categories)
            else:
                return Product.objects.filter(category__in=filtered_categories)





class ListRelatedView(APIView):
    """
    A view to retrieve products based on
    a productId's category and exclude a product associated productId
    for any user.

    url: api/products/related/<productId>
    Refactored statements: 2021/10/3
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id = int(productId)
        except:
            return Response({'error': 'Product ID must be an integer'},
                            status=status.HTTP_404_NOT_FOUND)


        # check a product whether it exists.
        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': 'Product with this product ID does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        category = Product.objects.get(id=product_id).category

        if Product.objects.filter(category=category).exists():

            # Refactored statements (Oct/3/2021)
            related_products = filter_by_category(category)
            related_products = ProductSerializer(related_products, many=True)


            # if product objects exist greater than 3, show 3 items.
            if len(related_products.data) > 3:
                return Response({'related_products': related_products.data[:3]},
                                status=status.HTTP_200_OK)

            # if product objects exists greater than 0, show all.
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
    A view retrieve ordered products based on date_created,
    sort_by, price_range, and sold for any user.

    url: api/products/by/search
    request: (int)category_id, (str)price_range,
            (str)sort_by, (str)order
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

        # check sort_by, default is date_created
        if not (sort_by == 'date_created' or sort_by == 'price' or
                sort_by == 'sold' or sort_by == 'name'):
            sort_by = 'date_created'

        if not sort_by:
            sort_by = 'date_created'

        order = data['order']

        # if category_id is 0, return all products
        if category_id == 0:
            product_results = Product.objects.all()

        elif not Category.objects.filter(id=category_id).exists():
            return Response({'error': 'This category does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        else:
            category = Category.objects.get(id=category_id)
            product_results = filter_by_category(category)

        # Filtering based on price_range
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

        # check order and sort_by, and apply filtering.
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






