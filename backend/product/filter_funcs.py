from .models import Product
from category.models import Category

"""
This file is created for code refactoring on Oct/3/2021.
"""



def filter_by_category(category, previous_results=None):
    """
    A function to filtering products based on product's category from
    'products/views.py'
    """

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



