from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.form  import CategoryForm,PageForm,UserProfile,UserForm,UserProfileForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
'''
django从1.9迁移到了2.0 将 django.urls
from django.core.urlresolvers import reverse 
'''
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    print("index")
    #测试浏览器是否支持cookie
    request.session.set_test_cookie()
    categorylist = Category.objects.order_by('-likes')[:5]
    pagelist = Page.objects.order_by('-views')[:5]
    #构建一个字典，作为上下文传递给模板引擎
    #blodmessage键对应于模板中的{{ boldmessage }}
    #模板上下文就是一个字典，将模板变量名映射到一个值上
    context_dict = {'boldmessage':"Crunchy, creamy, cookie, candy, cupcake!",
                    'categories':categorylist,
                    'pages':pagelist,

                    }
    visitor_cookie_handle(request)
    context_dict['visits'] = request.session['visits']
    response = render(request,'rango/index.html',context = context_dict)

    return response

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

@login_required
def add_category(request):
    form = CategoryForm()
    print("add!")
    #是HTTP POST请求吗？
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        #
        if form.is_valid():
            print(form)
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request,'rango/add_category.html',{'form':form})

def register(request):
    # 一个布尔值，告诉模板注册是否成功
    # 一开始设为 False，注册成功后改为 True
    registered = False
    # 如果是 HTTP POST 请求，处理表单数据
    if request.method == 'POST':
        # 尝试获取原始表单数据
        # 注意，UserForm 和 UserProfileForm 中的数据都需要
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # 如果两个表单中的数据是有效的……
        if user_form.is_valid() and profile_form.is_valid():
            # 把 UserForm 中的数据存入数据库
            user = user_form.save()
            # 使用 set_password 方法计算密码哈希值
            # 然后更新 user 对象
            user.set_password(user.password)
            user.save()
            # 现在处理 UserProfile 实例
            # 因为要自行处理 user 属性，所以设定 commit=False
            # 延迟保存模型，以防出现完整性问题
            profile = profile_form.save(commit=False)
            profile.user = user
            # 用户提供头像了吗？
            # 如果提供了，从表单数据库中提取出来，赋给 UserProfile 模型
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # 保存 UserProfile 模型实例
            profile.save()
            # 更新变量的值，告诉模板成功注册了
            registered = True
        else:
            # 表单数据无效，出错了？
            # 在终端打印问题
            print(user_form.errors, profile_form.errors)
    else:
        # 不是 HTTP POST 请求，渲染两个 ModelForm 实例
        # 表单为空，待用户填写
        user_form = UserForm()
        profile_form = UserProfileForm()
    # 根据上下文渲染模板
    return render(request,
                          'rango/register.html',
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    if request.method == 'POST':
        #获取表单的输入的用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')

        #使用django提供的函数检查用户名和密码是否有效，有效的话，返回一个user对象
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                #登入有效且激过的账户，然后重定向到首页
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                #账号没有激活
                context = {'message': 'Your Rango account is disables.'}
                return render(request,'rango/restricted.html',context)

        else:
            #用户密码错误
            context ={'message':'Invalid login details supplied.'}
            return render(request,'rango/restricted.html',context)

    #不是HTTP POST请求，显示登陆表单，极有可能是HTTP GET请求
    else:
        #没什么上下文变量要传给模板因此传入一个空字典
        return render(request,'rango/login.html',{})



@login_required
def restricted(request):
    context = {'message': "Since you're logged in ,you can see this text!"}
    return render(request, 'rango/restricted.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#辅助函数
def visitor_cookie_handle1(request,response):
    #获取网站的访问次数，如果visits存在，则转换为整数，如果不存在，赋值为1
    visits = int(request.COOKIES.get('visits','1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    #如果距离上次访问已经超过了一天
    if(datetime.now() - last_visit_time).days > 0:
        visits += 1
        response.set_cookie('last_visit',str(datetime.now()))
    else:
        response.set_cookie('last_visit',last_visit_cookie)

    response.set_cookie('visits',visits)

#
def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

#更新后的函数定义
def visitor_cookie_handle(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    #距离上次访问的时间超过了一天
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # 增加访问次数后更新“last_visit”cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        # 设定“last_visit”cookie
        request.session['last_visit'] = last_visit_cookie
    # 更新或设定“visits”cookie
    request.session['visits'] = visits