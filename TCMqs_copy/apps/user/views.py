from django.shortcuts import render,redirect
from django.urls import reverse
from  django.http import  HttpResponse
from  django.views.generic import View
from  django.conf import  settings
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers  import  make_password
import re
from  .models import  User
from  itsdangerous import  TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_task import tasks
# 验证码的实现
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from django.shortcuts import HttpResponse,render,redirect
# Create your views here.

#/user/register
def register(request):
    return  render(request, 'register.html')
#user/register_handle
def register_handle(request):

    #接受数据
    email = request.POST.get("inputEmail")
    password = request.POST.get("inputPassword")
    is_has_email=User.objects.filter(email__exact=email).first()
    # 进行数据校验
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
    if is_has_email:
        return render(request, 'register.html', {'errmsg': '用户已经存在'})
    if not all([email,password]):
        return  render(request,'register.html',{'errmsg':'数据不完整'})


    # 进行业务处理: 进行用户注册
    user = User.objects.create_user(username=email,email=email, password=password)
    user.is_active = 0
    user.save()
     #发送激活链接 /user/active/1
    # 加密用户的身份信息，生成激活token
    # serializer = Serializer(settings.SECRET_KEY, 600)
    # info = {'confirm': user.id}
    # token = serializer.dumps(info)  # bytes
    # token = token.decode()
    token=yield_code(settings.SECRET_KEY,user.id)
     #发送邮件
    try:

        tasks.send_register_email.delay(email,token)
    except :
        del_user=User.objects.get(id=user.id)
        del_user.delete()
        return HttpResponse("<h2>注册失败！请返回重新注册</h2>")
    # 返回应答, 跳转到登录页面
    return redirect(reverse('user:user_login'))

def  yield_code(code,user_id):
    # 加密用户的身份信息，生成激活token
    serializer = Serializer(code,120)
    info = {'confirm': user_id}
    token = serializer.dumps(info)  # bytes
    token = token.decode()
    return  token


class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''

        try:
            # 进行解密，获取要激活的用户信息
            serializer = Serializer(settings.SECRET_KEY, 600)
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            if user.is_active==1:
                return  HttpResponse("已激活，不用重复操作")
            user.is_active = 1

            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:user_login'))
        except SignatureExpired as e:
            # 激活链接已过期


            return HttpResponse('<h3>激活链接已过期：'+"<a href='http://4e9f10f.r2.cpolar.cn/user/to_active'>重新激活</a></h3>")


#again active
def again_active(request):
    return render(request,'active_user.html')

def again_active_handle(request):
    email=request.GET.get('email')
    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return  render(request,'active_user.html',{"errmsg":"用户已激活，请不要重复激活"})
        else:
            token=yield_code(settings.SECRET_KEY,user.id)
            tasks.send_register_email.delay(email, token)
            # 返回应答, 跳转到登录页面
            return redirect(reverse('user:user_login'))

    except:
        return render(request, 'active_user.html', {"errmsg": "用户不存在"})


class LoginView(View):
    # /user/login

    def get(self,request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'email' in request.COOKIES:
            email = request.COOKIES.get('email')
            checked = 'checked'
        else:
            email = ''
            checked = ''
        # 使用模板
        update_yanzheng(request)
        return render(request, 'user_login.html', {'email': email, 'checked': checked})
    def post(self,request):
        '''登录校验'''
        # 接收数据
        email= request.POST.get('InputEmail1')
        password = request.POST.get('InputPassword')
        username=email
        # 校验数据
        if not all([email,password]):
            update_yanzheng(request)
            return render(request, 'user_login.html', {'errmsg': '数据不完整'})
        user=authenticate(username=username,password=password)
        yanzheng = request.POST.get('yanzheng')
        if  not yanzheng :
            update_yanzheng(request)
            return render(request, 'user_login.html', {'errmsg': '验证码未填写'})
        code=request.session['code']

        print(code)
        if (yanzheng.strip()!=code.lower().strip())and (yanzheng.strip()!=code.upper().strip())and(yanzheng!=code):

            return render(request, 'user_login.html', {'errmsg': '验证码不正确'})
        if user is not None:
            if user.is_active:

                login(request,user)
                #跳转到首页
                #default index
                next=request.GET.get('next',reverse('tcm_query:tcm_query_index'))


                response=redirect(next)

                remember=request.POST.get('remember')
                if remember=='on':
                    response.set_cookie("email",email,max_age=24*3600)
                else:
                    response.delete_cookie('email')
                #跳转到首页
                return response
            else:
                update_yanzheng(request)
                return  render(request,'user_login.html',{'errmsg':'用户未激活'})
        else:
            # 用户名或密码错误
            update_yanzheng(request)
            return render(request, 'user_login.html', {'errmsg': '用户名或密码错误'})


class LoginOutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('user:user_login'))



#修改密码页面
def repair_password(request):
    return  render(request,'forget_password.html')

def repair_password_handle(request):
    # 接受数据
    email = request.POST.get("inputEmail")
    new_password = request.POST.get("inputPassword")
    is_has_email = User.objects.filter(email__exact=email).first()
    if not is_has_email:
        return render(request, 'forget_password.html', {'errmsg': '用户不存在'})
    else:
        is_has_email.password = make_password(new_password)
        is_has_email.save()
        print(new_password)
        # 返回应答, 跳转到登录页面
        return redirect(reverse('user:user_login'))
# 获取随机的样式颜色
def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
def get_code(request):
        img_obj = Image.new('RGB', (100, 30), get_random())  # 生成图片对象
        img_draw = ImageDraw.Draw(img_obj)  # 生成了一个画笔对象
        img_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoOblique.ttf', 20)
        # 随机码的获取：
        code = ''
        for i in range(5):
            upper_str = chr(random.randint(65, 90))  # ascii码 大写字母
            lower_str = chr(random.randint(97, 122))  # ascii码 小写字母
            random_int = str(random.randint(0, 9))
            tmp = random.choice([upper_str, lower_str, random_int])  # 随机取值

            img_draw.text((i * 12 + 12, 1), tmp, get_random(), img_font)  # 文字展示到图片上
            code += tmp  # 一次结果
        print(code)
        request.session['code'] = code  # 存储
        io_obj = BytesIO()  # 内存内存储，读取
        img_obj.save('static/img/yanzheng.png', 'png')  # 保存，并选定格式



def update_yanzheng(request):
    get_code(request)
    return render(request, 'user_login.html')







