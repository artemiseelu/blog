from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from .utils import generate_slug

class Category(models.Model):
    """文章分类模型"""
    name = models.CharField('分类名', max_length=100)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('描述', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['-created_time']

    def __str__(self):
        return self.name

class Article(models.Model):
    """文章模型"""
    # 文章状态选项
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='作者'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='分类'
    )
    content = models.TextField('内容')
    summary = models.TextField('摘要', max_length=500, blank=True)
    
    # 文章图片
    featured_image = models.ImageField(
        '特色图片',
        upload_to='articles/%Y/%m/',
        blank=True
    )
    
    # 时间相关字段
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    published_time = models.DateTimeField('发布时间', auto_now_add=True)
    
    # 状态
    status = models.CharField(
        '状态',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # 统计
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_time']  # 按发布时间倒序排序
        indexes = [
            models.Index(fields=['-published_time']),  # 添加索引提高查询性能
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """获取文章详情页URL"""
        return reverse('article_detail', args=[self.slug])

    def increase_views(self):
        """增加浏览量"""
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        """重写save方法，确保生成slug"""
        if not self.slug and self.title:
            self.slug = generate_slug(self.title)
            
            # 确保slug唯一
            base_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
            
        if not self.summary and self.content:
            self.summary = self.content[:200]
        
        super().save(*args, **kwargs)
