from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page


def index(request):
    categorylist = Category.objects.order_by('-likes')[:5]
    pagelist = Page.objects.order_by('-views')[:5]
    #构建一个字典，作为上下文传递给模板引擎
    #blodmessage键对应于模板中的{{ boldmessage }}
    #模板上下文就是一个字典，将模板变量名映射到一个值上
    context_dict = {'boldmessage':"Crunchy, creamy, cookie, candy, cupcake!",
                    'categories':categorylist,
                    'pages':pagelist
                    }


    return render(request,'rango/index.html',context = context_dict)


def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}
    try:
        # 能通过传入的分类别名找到对应的分类吗？
        # 如果找不到，.get() 方法抛出 DoesNotExist 异常
        # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)
        # 检索关联的所有网页
        # 注意，filter() 返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)
        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages
        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None
        # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)