from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Review
from product.models import Product

# Get multiple reviews related to product_id
class GetProductReviewsView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': 'This product does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)

            # use a list since we store multiple review data
            results = []

            if Review.objects.filter(product=product).exists():
                reviews = Review.objects.order_by('-date_created').filter(product=product)

                # iterate a Queryset
                for review in reviews:
                    item = {}
                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)


            return Response({'reviews': results},
                            status=status.HTTP_200_OK)

        except:
            return Response(
                {'error': 'Error in GetProductReviewsView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Get a single review related to product_id, allow to only registered users.
class GetProductReviewView(APIView):
    def get(self, request, productId, format=None):
        user = self.request.user

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': 'This product does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)

            result = {}

            if Review.objects.filter(user=user, product=product_id).exists():
                review = Review.objects.get(user=user, product=product)

                # Store a review
                result['id'] = review.id
                result['rating'] = review.rating
                result['comment'] = review.comment
                result['date_created'] = review.date_created
                result['user'] = review.user.first_name

            
            return Response({'review': result},
                            status=status.HTTP_200_OK)

        except:
            return Response(
                {'error': 'Error in GetProductReviewView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# only registered user can create a review
class CreateProductReviewView(APIView):
    def post(self, request, productId, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(productId)
        except:
            return Response(
                {'error': 'Product ID must be interger'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            rating = float(data['rating'])
        except:
            return Response(
                {'error': 'Rating must be float type.'},
                status=status.HTTP_400_BAD_REQUEST
            )


        try:
            comment = str(data['comment'])
        except:
            return Response({'error': 'Must pass a comment when creating a review'},
                            status=status.HTTP_400_BAD_REQUEST)


        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error': 'This product does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)


            # return a created review and all reviews
            result = {}
            results = []

            # Each user can make only one review by each product.
            if Review.objects.filter(user=user, product=product_id).exists():
                return Response({'error': 'A review for this product already existed.'},
                                status=status.HTTP_409_CONFLICT)


            # Create a review object and store to 'review'
            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment
            )

            # Exceptions for zero comment


            # Pass created 'review' to result dict
            if Review.objects.filter(user=user, product=product_id).exists():
                result['id'] = review.id
                result['rating'] = review.rating
                result['comment'] = review.comment
                result['date_created'] = review.date_created
                result['user'] = review.user.first_name

            # Bring all reviews
                reviews = Review.objects.order_by('-date_created').filter(
                    product=product_id
                )


                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)


            return Response({'review': result, 'reviews': results},
                            status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Error in CreateReviewView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProductReviewView(APIView):
    def put(self, request, productId, format=None):
        user = self.request.user
        data = self.request.data

        try:
            product_id = int(productId)
        except:
            return Response({'error': 'Product Id must be integer.'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            rating = float(data['rating'])
        except:
            return Response({'error': 'Rating must be float type'},
                            status=status.HTTP_400_BAD_REQUEST)


        try:
            comment = str(data['comment'])
        except:
            return Response({'error': 'Must pass a comment when creating a review'},
                            status=status.HTTP_400_BAD_REQUEST)


        # check whether product_id and user exist, and update.
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response(
                    {'error': 'This product does not exists'},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.get(id=product_id)
            result = {}
            results = []


            if not Review.objects.filter(product=product_id, user=user).exists():
                return Response(
                    {'error': 'The review related to this product does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if Review.objects.filter(user=user, product=product_id).exists():
                Review.objects.filter(user=user, product=product_id).update(
                    rating=rating,
                    comment=comment
                )
                review = Review.objects.get(user=user, product=product)

                result['id'] = review.id
                result['rating'] = review.rating
                result['comment'] = review.comment
                result['date_created'] = review.date_created
                result['user'] = review.user.first_name

                # Bring all reviews related to the product
                reviews = Review.objects.order_by('-date_created').filter(product=product_id)

                for review in reviews:
                    item = {}

                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

            return Response({'review': result, 'reviews': results},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Error in UpdateReviewView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete a review related to a product
class DeleteProductReviewView(APIView):
    def delete(self, request, productId, format=None):
        user = self.request.user

        try:
            product_id = int(productId)

        except:
            return Response({'error': 'Product Id must be integer.'},
                            status=status.HTTP_404_NOT_FOUND)


        # check whether product does exist
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error:': 'This product does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)

            # get과 filter 비교

            if Review.objects.filter(user=user, product=product).exists():

                Review.objects.filter(product=product, user=user).delete()
                results = []

                if Review.objects.filter(product=product).exists():
                    reviews = Review.objects.order_by('-date_created').filter(product=product_id)

                    for review in reviews:
                        item = {}

                        item['id'] = review.id
                        item['rating'] = review.rating
                        item['comment'] = review.comment
                        item['date_created'] = review.date_created
                        item['user'] = review.user.first_name

                        results.append(item)

                return Response({'Reviews': results},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error:': 'A review for this product does not exist'},
                                status=status.HTTP_404_NOT_FOUND)


        except:
            return Response({'error':'Error in DeleteProductReviewView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# By rating, filtering reviews. Any user can access it.
# rating range: 0.5 - 5.0 // multiples of 0.5
class FilterProductReviewView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):

        # Check product_id whether is integer
        try:
            product_id = int(productId)
        except:
            return Response({'error': 'Product Id must be integer'},
                            status=status.HTTP_404_NOT_FOUND)


        # Check a product exists
        if not Product.objects.filter(id=product_id).exists():
            return Response({'error': 'This product does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.get(id=product_id)

        rating = request.query_params.get('rating')

        # Check a type of rating
        try:
            rating = float(rating)

        except:
            return Response({'error': 'Rating must be float type'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if not rating:
                rating = 5.0
            elif rating > 5.0:
                rating = 5.0
            elif rating < 0.5:
                rating = 0.5

            results = []


            if Review.objects.filter(product=product).exists():
                if rating == 0.5:
                    reviews = Review.objects.order_by('-date_created').filter(
                        rating=rating, product=product
                    )

                # suppose rating is 2.5
                # including rating with 2.5 and 2.0 by subtracting 0.5
                else:
                    reviews = Review.objects.order_by('-date_created').filter(
                        rating__lte=rating, product=product
                    ).filter(
                        rating__gte=(rating - 0.5),
                        product=product
                    )

                for review in reviews:
                    item = {}
                    item['id'] = review.id
                    item['rating'] = review.rating
                    item['comment'] = review.comment
                    item['date_created'] = review.date_created
                    item['user'] = review.user.first_name

                    results.append(item)

                return Response({'reviews': results},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'The review for the product does not exist'},
                                status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'error':'Error in FilteringProductReviewView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




