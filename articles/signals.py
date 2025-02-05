from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Article

@receiver(pre_save, sender=Article)
def create_slug(sender, instance, **kwargs):
    """在保存文章前自动生成 slug"""
    if not instance.slug:
        instance.slug = slugify(instance.title)

    # 如果生成的 slug 已存在，添加数字后缀
    if instance.pk is None:  # 新创建的文章
        original_slug = instance.slug
        counter = 1
        while Article.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

@receiver(pre_save, sender=Article)
def create_summary(sender, instance, **kwargs):
    """在保存文章前自动生成摘要"""
    if not instance.summary and instance.content:
        # 取内容的前200个字符作为摘要
        instance.summary = instance.content[:200] 