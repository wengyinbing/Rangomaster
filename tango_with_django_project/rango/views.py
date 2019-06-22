from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    #构建一个字典，作为上下文传递给模板引擎
    #blodmessage键对应于模板中的{{ boldmessage }}
    #模板上下文就是一个字典，将模板变量名映射到一个值上
    context_dict = {'boldmessage':"Crunchy, creamy, cookie, candy, cupcake!"}

    return render(request,'rango/index.html',context = context_dict)
