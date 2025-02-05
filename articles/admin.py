from django.contrib import admin
from .models import Article, Category
from .utils import generate_slug

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        """重写保存方法，处理中文 slug"""
        if not change:  # 只在创建新分类时生成 slug
            if not obj.slug and obj.name:
                obj.slug = generate_slug(obj.name)
        super().save_model(request, obj, form, change)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_time', 'category', 'views']
    list_filter = ['published_time', 'category']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_time'

    def save_model(self, request, obj, form, change):
        """重写保存方法，处理中文 slug"""
        if not change:  # 只在创建新文章时生成 slug
            if not obj.slug and obj.title:
                base_slug = generate_slug(obj.title)
                slug = base_slug
                counter = 1
                
                # 检查 slug 是否存在
                while Article.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}_n{counter}"
                    counter += 1
                
                obj.slug = slug
        super().save_model(request, obj, form, change)

    class Media:
        js = ('js/admin/slug_generator.js',)  # 添加自定义 JS
