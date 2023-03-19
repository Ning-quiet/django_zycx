from django.urls import path,re_path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'tcm_query'
urlpatterns = [
    path('index', views.BannerInedx.as_view(), name='tcm_query_index'),
    path('query',login_required(views.QueryListview.as_view()),name='tcm_query_query'),
    path('query/search',views.ajax_search,name='tcm_query_search'),
    path('query/search_eff', views.ajax_search_eff, name='tcm_query_search_eff'),
    path('detail/<int:pk>/', views.TcmDetailView.as_view(), name='detail'),
    path('shibie',views.tcm_shibie_show,name='tcm_shibie'),
    path('handle_img',views.tcm_handle_img,name='handle_img'),
    path('handle_shuju', views.shuju, name='shuju'),
    path('', views.BannerInedx.as_view(), name='tcm_query_index_1'),

]