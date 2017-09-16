from django.contrib import admin
from .models import Article, Tag, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'create_date'

    exclude = ('author',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('title', 'author', 'create_date', 'status', 'category')

    # 激活过滤器，这个很有用
    list_filter = ('author', 'create_date', 'category', 'status')

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    filter_horizontal = ('tags',)  # 给多选增加一个左右添加的框

    # 重写保存函数，把文章作者自动跟登录用户绑定
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = 'Stopfollow 个人博客'