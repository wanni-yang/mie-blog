import markdown

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

class Category(models.Model):
    """
    blog 分类表，继承model.Model类
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签表 Tag 也比较简单，和 Category 一样。
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """

    # 文章标题
    title = models.CharField('标题',max_length=70)

    # 文章正文
    body = models.TextField('正文')

    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此使用 models.CASCADE 参数，意为级联删除。
    # category和post之间是1对多的关系，用ForeignKey关联
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)

    # tags和post之间是多对多的关系，用ManyToManyField关联
    tags = models.ManyToManyField(Tag,  verbose_name='标签', blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是django 为我们已经写好的用户模型。
    # author和post之间是1对多的关系，用ForeignKey关联
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 自动生成摘要
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 以执行数据保存回数据库的逻辑
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mieblog:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title