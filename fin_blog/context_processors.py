from .models import Category


def categories_processor(request):
    categories = Category.objects.filter(approved=True)
    return {'categories': categories}
