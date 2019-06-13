from django import template

register = template.Library()


@register.filter(name='extract_text')  # 过滤器在模板中使用时的name
def extract_text(value):
    from bs4 import BeautifulSoup
    bs = BeautifulSoup(value, "html.parser")
    return bs.get_text()[0:30]
