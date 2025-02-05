from django import forms
from .models import Article, Category
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models import Q
from .utils import generate_slug

class ArticleForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'featured_image', 'summary', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入文章标题'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '请输入文章内容'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请输入文章摘要（可选）'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_title(self):
        """验证标题并生成slug"""
        title = self.cleaned_data['title']
        
        # 只在创建新文章时检查 slug 是否存在
        if not self.instance.pk:  # 新文章
            slug = generate_slug(title)
            if Article.objects.filter(slug=slug).exists():
                raise ValidationError('该标题生成的URL已存在，请修改标题。')
        
        return title
    
    def save(self, commit=True):
        """重写save方法，确保生成slug"""
        article = super().save(commit=False)
        
        # 只在创建新文章时生成 slug
        if not article.pk and article.title:  # 新文章且有标题
            base_slug = generate_slug(article.title)
            slug = base_slug
            counter = 1
            
            # 检查slug是否存在，如果存在则添加数字后缀
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}_n{counter}"
                counter += 1
            
            article.slug = slug
        
        if commit:
            article.save()
        return article

class ArticleFilterForm(forms.Form):
    """文章筛选表单"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="所有分类",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', '所有状态')] + list(Article.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    def clean(self):
        """重写clean方法，添加自定义验证逻辑"""
        cleaned_data = super().clean()
        # 添加自定义验证逻辑
        return cleaned_data

    def save(self, commit=True):
        """重写save方法，自动生成slug"""
        article = super().save(commit=False)
        article.slug = slugify(article.title)
        
        if commit:
            article.save()
        return article

class ArticleFilterFormPublic(forms.Form):
    """公共文章筛选表单（不包含状态筛选）"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '搜索文章...',
            'aria-label': '搜索'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="所有分类",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-label': '分类'
        })
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'aria-label': '开始日期'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'aria-label': '结束日期'
        })
    )

class ArticleFilterForm(ArticleFilterFormPublic):
    """完整的文章筛选表单（包含状态筛选）"""
    status = forms.ChoiceField(
        choices=[('', '所有状态')] + list(Article.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-label': '状态'
        })
    ) 