from .models import Category


def category_list(request):
    categories = Category.objects.filter(approved=True).order_by('name')
    return {'categories': categories}
