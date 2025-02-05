from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q, F
from .models import Article, Category
from .forms import ArticleForm, ArticleFilterForm, ArticleFilterFormPublic
from django.utils.text import slugify
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, DetailView
from django.utils.translation import activate

# Create your views here.

class BaseView:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取语言参数
        lang = self.request.GET.get('lang', 'cn')
        activate(lang)  # 激活选择的语言
        return context

class ArticleListView(BaseView, ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

class ArticleDetailView(BaseView, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

def home(request):
    """首页视图"""
    lang = request.GET.get('lang', 'cn')
    activate(lang)
    # 获取阅读量前三的文章
    top_articles = Article.objects.order_by('-views')[:3]
    return render(request, 'home.html', {'top_articles': top_articles})

def article_list(request):
    """文章列表视图"""
    # 根据用户登录状态过滤文章
    if request.user.is_authenticated:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(status='published')
    
    print(f"文章数量: {articles.count()}")  # 调试信息
    for article in articles:
        print(f"标题: {article.title}, 状态: {article.status}, Slug: {article.slug}, ID: {article.id}")
    
    # 根据用户登录状态创建不同的筛选表单
    if request.user.is_authenticated:
        filter_form = ArticleFilterForm(request.GET)
    else:
        filter_form = ArticleFilterFormPublic(request.GET)
    
    # 应用筛选
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        category = filter_form.cleaned_data.get('category')
        if request.user.is_authenticated:
            status = filter_form.cleaned_data.get('status')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        # 搜索功能
        if search:
            articles = articles.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(summary__icontains=search)
            )
        
        if category:
            articles = articles.filter(category=category)
        if request.user.is_authenticated and status:
            articles = articles.filter(status=status)
        if date_from:
            articles = articles.filter(published_time__date__gte=date_from)
        if date_to:
            articles = articles.filter(published_time__date__lte=date_to)
    
    # 分页
    paginator = Paginator(articles, 9)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'articles': articles,
        'filter_form': filter_form,
        'is_authenticated': request.user.is_authenticated,  # 传递登录状态到模板
    }
    return render(request, 'articles/list.html', context)

def article_detail(request, slug):
    """文章详情视图"""
    try:
        article = get_object_or_404(Article, slug=slug)
        if not article.slug:  # 如果没有slug，生成一个
            article.save()  # 这会触发save方法生成slug
            
        article.increase_views()  # 增加浏览量
        
        # 获取相关文章 - 只获取有效的文章
        related_articles = Article.objects.filter(
            category=article.category,
            status='published'  # 只获取已发布的文章
        ).exclude(
            id=article.id
        ).exclude(
            slug=''  # 排除没有slug的文章
        )[:3]
        
        context = {
            'article': article,
            'related_articles': related_articles
        }
        return render(request, 'articles/detail.html', context)
    except Article.DoesNotExist:
        messages.error(request, '文章不存在！')
        return redirect('article_list')

@login_required
def article_upload(request):
    """发布文章视图"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            
            # 确保生成slug
            if not article.slug and article.title:
                article.slug = slugify(article.title)
                
                # 确保slug唯一
                base_slug = article.slug
                counter = 1
                while Article.objects.filter(slug=article.slug).exists():
                    article.slug = f"{base_slug}-{counter}"
                    counter += 1
            
            article.save()
            messages.success(request, '文章发布成功！')
            return redirect('article_detail', slug=article.slug)
        else:
            messages.error(request, '表单验证失败，请检查输入。')
    else:
        form = ArticleForm()
    
    return render(request, 'articles/upload.html', {'form': form})

@login_required
def article_edit(request, slug):
    """编辑文章视图"""
    try:
        article = get_object_or_404(Article, slug=slug)
        
        # 检查权限
        if article.author != request.user and not request.user.is_superuser:
            messages.error(request, '你没有权限编辑这篇文章！')
            return redirect('article_list')
        
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                # 保存原始slug
                original_slug = article.slug
                article = form.save(commit=False)
                
                # 如果标题改变了，更新slug
                if slugify(article.title) != original_slug:
                    article.slug = slugify(article.title)
                
                article.save()
                messages.success(request, '文章更新成功！')
                return redirect('article_detail', slug=article.slug)
        else:
            form = ArticleForm(instance=article)
        
        return render(request, 'articles/upload.html', {
            'form': form,
            'article': article,
            'edit_mode': True
        })
    except Article.DoesNotExist:
        messages.error(request, '文章不存在！')
        return redirect('article_list')

@login_required
def article_delete(request, slug):
    """删除文章视图"""
    article = get_object_or_404(Article, slug=slug, author=request.user)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, '文章已删除！')
        return redirect('article_list')
    
    return render(request, 'articles/delete_confirm.html', {'article': article})

@staff_member_required
def generate_slug_view(request):
    """为管理后台生成 slug 的视图"""
    title = request.GET.get('title', '')
    slug = generate_slug(title)
    return JsonResponse({'slug': slug})

def resume(request):
    """简历页面视图"""
    # 测试数据
    context = {
        'personal_info': {
            'name': '张三',
            'title': '全栈开发工程师',
            'avatar': 'images/default-avatar.png',
            'email': 'zhangsan@example.com',
            'phone': '138xxxx8888',
            'location': '北京市朝阳区',
            'github': 'https://github.com/zhangsan',
            'linkedin': 'https://linkedin.com/in/zhangsan',
            'summary': '5年全栈开发经验，专注于Python/Django开发，\
                      熟悉前端技术栈，具有良好的代码风格和团队协作能力。'
        },
        'skills': [
            {'name': 'Python/Django', 'level': 90},
            {'name': 'JavaScript/Vue', 'level': 85},
            {'name': 'HTML/CSS', 'level': 88},
            {'name': 'PostgreSQL', 'level': 82},
            {'name': 'Docker', 'level': 75},
            {'name': 'Linux', 'level': 80},
        ],
        'experience': [
            {
                'company': 'XX科技有限公司',
                'title': '高级开发工程师',
                'period': '2020-至今',
                'description': [
                    '负责公司核心业务系统的开发和维护',
                    '优化系统性能，将接口响应时间降低50%',
                    '带领5人团队完成多个重要项目',
                ],
            },
            {
                'company': 'YY互联网公司',
                'title': '开发工程师',
                'period': '2018-2020',
                'description': [
                    '参与电商平台的开发',
                    '实现订单系统重构',
                    '编写技术文档和单元测试',
                ],
            },
        ],
        'projects': [
            {
                'name': '企业资源管理系统',
                'period': '2021-2022',
                'description': '使用Django开发的企业级管理系统，\
                              包含人事、财务、库存等模块',
                'technologies': ['Python', 'Django', 'Vue.js', 'PostgreSQL'],
            },
            {
                'name': '在线教育平台',
                'period': '2020-2021',
                'description': '支持在线课程发布、视频播放、作业管理等功能',
                'technologies': ['Django REST framework', 'React', 'Redis'],
            },
        ],
        'education': [
            {
                'school': 'XX大学',
                'degree': '计算机科学与技术 学士',
                'period': '2014-2018',
                'description': '主修课程：数据结构、算法、计算机网络、数据库等',
            }
        ]
    }
    return render(request, 'articles/resume.html', context)

def resume2(request, lang='cn'):
    if lang == 'en':
        context = {
            'personal_info': {
                'name': 'John Doe',
                'title': 'Software Developer',
                'avatar': 'images/avatar.jpg',
                'email': 'john.doe@email.com',
                'phone': '0123 456789',
                'location': 'New York',
                'github': 'github.com/johndoe',
                'linkedin': 'linkedin.com/in/johndoe',
                'summary': 'Hi, my name is John Doe...',
            },
            'sections': {
                'about': 'About Me',
                'skills': 'Skills',
                'contact': 'Contact',
                'experience': 'Experience',
                'projects': 'Projects',
                'education': 'Education',
            },
        }
    else:
        context = {
            'personal_info': {
                'name': '张三',
                'title': '资深算法工程师',
                'avatar': 'images/avatar.jpg',
                'email': 'artemiseelu@gmail.com',
                'phone': '0123 456789',
                'location': '北京',
                'github': 'github.com/johndoe',
                'linkedin': 'linkedin.com/in/jiaxing-lu-6a0a16b4/',
                'summary': '你好，我是张三...',
            },
            'skills': [
            {'name': 'Python/Django', 'level': 90},
            {'name': 'JavaScript/Vue', 'level': 85},
            {'name': 'HTML/CSS', 'level': 88},
            {'name': 'PostgreSQL', 'level': 82},
            {'name': 'Docker', 'level': 75},
            {'name': 'Linux', 'level': 80},
        ],
            'sections': {
                'about': '关于我',
                'skills': '技能专长',
                'contact': '联系方式',
                'experience': '工作经历',
                'projects': '项目经验',
                'education': '教育背景',
            },
        }
    
    context['current_lang'] = lang
    return render(request, 'articles/resume2.html', context)
