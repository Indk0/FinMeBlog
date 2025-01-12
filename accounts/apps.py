from django.apps import AppConfig


# Configuration class for the accounts app
class AccountsConfig(AppConfig):
    # Default primary key field type
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # Name of the app
