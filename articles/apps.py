from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"
    verbose_name = "文章管理"

    def ready(self):
        try:
            import articles.signals
            print("Signals registered successfully")
        except ImportError:
            print("Failed to register signals")
