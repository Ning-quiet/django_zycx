from django.urls import path,re_path
from  . import  views
from .views import  ActiveView,LoginView,LoginOutView
app_name = 'user'
urlpatterns = [
    path(r'register_handle', views.register_handle, name='register_handle'),
    path(r'register',views.register,name='register'),
    path(r'to_active',views.again_active,name='again_active'),
    path(r'active_handle',views.again_active_handle,name="again_active_handle"),
    path(r'repair_pass',views.repair_password,name="repair_password"), #页面调转
    path(r'repair_pass_handle',views.repair_password_handle,name="repair_password_handle"),
    re_path(r'login$',LoginView.as_view(),name="user_login"), #登录 校验处理
     path('logout',LoginOutView.as_view(),name='login_out'),
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活

    # path('update_yanzheng/', views.update_yanzheng),  # 验证码替换
]
