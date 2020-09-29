from django import template

from ..models import Post, Category, Tag

register = template.Library()

@register.inclusion_tag('mieblog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    """
    :param context: 最新文章模板标签
    :param num:
    :return:
    """
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('mieblog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    """
    :param context: 归档模板标签
    :param num:
    :return:
    """
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }

@register.inclusion_tag('mieblog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    """
    :param context: 分类模板标签
    :param num:
    :return:
    """
    return {
        'category_list': Category.objects.all(),
    }

@register.inclusion_tag('mieblog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    """
    :param context: 标签云模板标签
    :param num:
    :return:
    """
    return {
        'tag_list': Tag.objects.all(),
    }