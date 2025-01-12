from .models import Category

# Context processor to provide approved categories to all templates


def categories_processor(request):
    categories = Category.objects.filter(
        approved=True)  # Fetch only approved categories
    return {'categories': categories}  # Add categories to the context
