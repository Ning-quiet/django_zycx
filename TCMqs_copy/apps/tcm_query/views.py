# coding=utf-8
from django.shortcuts import get_object_or_404,get_list_or_404,render
from  .models import  TcmDetailInfomations,Banner,CheseHerbsShow,TcmPic
from django.views import generic
from django.db.models import Q
import datetime
from django.http import JsonResponse
import base64
import  random
from django.contrib.auth.decorators import login_required
# 在具体的每个页面添加

class  BannerInedx(generic.ListView):
    model = Banner
    template_name = 'tcm_query/index.html'
    context_object_name = 'banner'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BannerInedx, self).get_context_data(**kwargs)
        show_list=[]
        show_obj=CheseHerbsShow.objects.filter(is_show=1)
        for show in show_obj:
                show_list.append(show.id)

        random.shuffle(show_list)

        chese_herb_show=CheseHerbsShow.objects.filter(id__in=show_list[:3]) #可以随机显示
        context['chese_herb_show']=chese_herb_show
        banner_list = Banner.objects.filter(is_show=1)
        # 最hot
        tcm_new=TcmDetailInfomations.objects.filter(view_count=0)[:4]
        #最新
        cur_time = datetime.datetime.now()  # 如果数据库保存的是UTC时间,程序不会蹦但是会提示你这不是本地时间

        now_time_utc = datetime.datetime.utcnow()
        # 当前天 显示当前日期是本周第几天
        day_num = cur_time.isoweekday()
        # 计算当前日期所在周一
        monday = (cur_time - datetime.timedelta(days=day_num))
        # 查询一周内的数据
        # all_datas = YourModel.objects.filter(time__range=(now_time, monday))
        tcm_hot=TcmDetailInfomations.objects.filter(Q(view_count__lt=10)|Q(create_time__range=(now_time_utc,monday))).order_by('create_time')[:4]
        context['tcm_hot']=tcm_hot
        context['tcm_new']=tcm_new

        context['banner_list'] = banner_list

        return context

    # def get_queryset(self):
    #     self.c = self.request.GET.get("c", None)
    #     if self.c:
    #         classification = get_object_or_404(Classification, pk=self.c)
    #         return classification.video_set.all().order_by('-create_time')
    #     else:
    #         return Video.objects.filter(status=0).order_by('-create_time')


class QueryListview(generic.ListView):
    model = TcmDetailInfomations
    template_name = 'tcm_query/tcm_qurty.html'
    context_object_name = 'tcm_detail_info'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QueryListview, self).get_context_data(**kwargs)
        liangxing=TcmDetailInfomations.objects.get_liangxing()
        rexing=TcmDetailInfomations.objects.get_rexing()
        hanxing= TcmDetailInfomations.objects.get_hanxing()
        wenxing=TcmDetailInfomations.objects.get_wenxing()
        pingxing=TcmDetailInfomations.objects.get_pingxing()
        context['liangxing']=liangxing
        context['rexing']=rexing
        context['hanxing']=hanxing
        context['wenxing']=wenxing
        context['pingxing']=pingxing
        context['tcm_detail_medicinal_part_ca']=TcmDetailInfomations.objects.get_all()
        context['tcm_detail_yaoming']=TcmDetailInfomations.objects.get_yaoming()
        context['tcm_detail_gongxiao']=TcmDetailInfomations.objects.get_gongxiao()
        context['tcm_detail_guijing']=TcmDetailInfomations.objects.get_guijing()
        return  context



    def get_queryset(self):
        self.c = self.request.GET.get("c", None)


#ajax 搜索请求
def ajax_search(request):

    input=request.POST.get('input_tcm')
    tcm_obj_list = []
    if input !=''  and input is not  None:
        tcm_obj=TcmDetailInfomations.objects.filter(Q(tcm_title__contains=input)|Q(alias__contains=input)|Q(scientific_name__contains=input)|Q(family_name__contains=input))

        if tcm_obj:
            for item in tcm_obj:
                tcm_obj_list.append({"title":item.tcm_title,"id":item.id})
    return JsonResponse(tcm_obj_list, safe=False)
def ajax_search_eff(request):
    tcm_obj_list = []
    input = request.POST.get('input_tcm_eff')
    if input !='' and  input is not  None:
        tcm_obj = TcmDetailInfomations.objects.filter(
            Q(efficacy_function__contains=input) | Q(efficacy_category__contains=input) | Q(channel_entry__contains=input))

        if tcm_obj:
            for item in tcm_obj:
                tcm_obj_list.append({"title": item.tcm_title, "id": item.id})


    return  JsonResponse(tcm_obj_list,safe=False)
class TcmDetailView(generic.DetailView):
    model = TcmDetailInfomations
    template_name = 'tcm_query/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super(TcmDetailView, self).get_context_data(**kwargs)
        recommend_list = TcmDetailInfomations.objects.get_recommend_list()
        context['recommend_list'] = recommend_list
        return context
#中药图片识别
@login_required
def  tcm_shibie_show(request):
    return render(request,'tcm_query/tcn_pic_shibie.html')


def tcm_handle_img(request):
     # client_id 为官网获取的AK(API Key)， client_secret 为官网获取的SK(Secret Key)
     try:
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
        file_img = request.FILES['img']
        print(file_img.file)
        img = base64.b64encode(file_img.file.getvalue())
        api_key = 'xVqCL5EGA9zo671yh8rEhMHE'
        client_secrect = 'enYtQclcLgF6zjfXdghdDfs0RgLW7tBY'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + api_key + '&client_secret=' + client_secrect
        response = requests.get(host)
        access_token = ''
        if response:
            access_token = response.json()['access_token']
        params = {"image": img,'baike_num':3}
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            r=response.json()

        print(r)
        print(type(r))

        return  render(request,'tcm_query/tcn_pic_shibie.html',{'result':r})
     except Exception as e:
        print(e)
        return JsonResponse('error requests',safe=False)
import requests
from lxml import etree
class ZySpider:
    def __init__(self, page):
        self.page= page
        self.start_url ='https://www.dayi.org.cn/list/5?pageNo='+self.page
        self.part_url = "https://www.dayi.org.cn"
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

    def parse_url(self, url):
        response = requests.get(url, headers=self.header)
        response.encoding=response.apparent_encoding
        return response.text
    def save_img(self,img_url,name):
        response=requests.get(img_url, headers=self.header)
        with open("./upload/tcm_pic/"+name+'.png', "wb")as f1:
            f1.write(response.content)

            print("保存完成！")
            return  'tcm_pic/'+name+'.png'

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@class='text_name']")
        content_list_url= []
        list_str = []
        for div in div_list:
             content_list_url.append(self.part_url+div.xpath("./a/@href")[0])
        for part_url in content_list_url:
            content_str=self.parse_url(part_url)
            html_1=etree.HTML(content_str)
            #中药名称
            tcm_title=html_1.xpath("//div/span[@class='name']/text()")[0]
            print('名称：'+tcm_title)

            desc_tail=html_1.xpath("//div/p[@class='intro']//text()")
            desc_tail_str= desc_tail[0] if len(desc_tail)>0 else ''
            print('详细表述：',desc_tail_str)

            func_cata=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[2]/div/div[2]//text()")
            func_cata_str=func_cata[0] if len(func_cata)>0 else ''

            zuzhi_func=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[3]/div/div[2]/p//text()")
            zuzhi_func_str=zuzhi_func[0] if len(zuzhi_func)>0 else ""

            # yongfayongmliang=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[4]/div/div[2]/text()")
            # yongfayongmliang_str= yongfayongmliang[0] if len(yongfayongmliang)>0 else ''
            # print('用法用量',yongfayongmliang)
            # zhuyi=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[7]/div/div[2]/text()")
            # zhuyi_str=zhuyi[0] if len(zhuyi)>0 else ""
            # print('注意事项',zhuyi)
            linchuang=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[2]/div[2]/div/div[2]//text()")
            linchuang_str=linchuang[0] if len(linchuang)>0 else ''

            source=html_1.xpath('//*[@id="global"]/div[2]/div/div[2]/article/div/div[3]/section[5]/div[4]/div/div[2]/text()')
            source_str=source[0] if len(source)>0 else ''


            img=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/aside/div[1]/img/@src")
            img_url=img[0].split('?')[0]
            print(img_url)
            image=self.save_img(img_url,tcm_title)

            shuju=(tcm_title,func_cata_str+'\n'+zuzhi_func_str,desc_tail_str+'\n'+linchuang_str,source_str,image)
            list_str.append(shuju)
        return list_str

    def run(self):
        html_str=self.parse_url(self.start_url)
        return  self.get_content_list(html_str)

class Spider:

    def __init__(self, page):
        self.page = page
        self.start_url = 'https://m.zhongyoo.com/name/page_'+self.page+'.html'
        self.part_url = "http://m.zhongyoo.com"
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

    def parse_url(self, url):
        response = requests.get(url, headers=self.header)
        #
        return response.content

    def save_img(self, img_url, name):
        response = requests.get(img_url, headers=self.header)
        with open("./upload/tcm_pic/" + name + '-1.jpg', "wb")as f1:
            f1.write(response.content)
            print("保存完成！")
        return    'tcm_pic/'+name+'-1.jpg'


    def replace_str(self,str1):
        return  str1.replace('】','')

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//*[@id='center']/article[3]/ul/li/@onclick")
        content_list_url = []
        for div in div_list:
            part_url=div.split('=')[1]
            part_url=part_url.replace("'","")
            print(part_url)
            content_list_url.append(part_url)
        print(content_list_url)
        content=[]
        for url in content_list_url:
            html_1_str=self.parse_url(url)
            html_1=etree.HTML(html_1_str)
            mingcheng=html_1.xpath('//*[@id="art_text"]/div/p[1]//text()')
            mingcheng_str=''.join(mingcheng).split('】')
            mingcheng_str=mingcheng_str[1]



            bieming=html_1.xpath('//*[@id="art_text"]/div/p[2]//text()')
            bieming_str=''.join(bieming).split('】')[1]

            keming = html_1.xpath('//*[@id="art_text"]/div/p[4]//text()')
            keming_str = ''.join(keming).split('】')[1]



            zhiwuxingtai=html_1.xpath('//*[@id="art_text"]/div/p[5]/text()[2]')
            zhiwuxingtai_str=self.replace_str(zhiwuxingtai[0])

            source=html_1.xpath('//*[@id="art_text"]/div/p[6]/text()[2]')
            source_str=self.replace_str(source[0])

            yaoxaixingzhuang=html_1.xpath('//*[@id="art_text"]/div/p[8]//text()')
            yaoxaixingzhuang_str=''.join(yaoxaixingzhuang)

            xingwei_obj=html_1.xpath('//*[@id="art_text"]/div/p[9]//text()')
            fenzhu=''.join(xingwei_obj).split('】')[1]


            guijiung = fenzhu.split('。')[1]
            yaoxing = fenzhu.split('。')[0].split('，')[0]
            wuwei = fenzhu.split('。')[0].split('，')[1]

            eff_function=html_1.xpath('//*[@id="art_text"]/div/p[10]/text()[2]')
            eff_function_str=self.replace_str(eff_function[0])

            lichuang=html_1.xpath('//*[@id="art_text"]/div/p[11]//text()')
            lichuang_str=''.join(lichuang)

            shiyongjinji=html_1.xpath('//*[@id="art_text"]/div/p[14]//text()')
            shiyongjinji_str=''.join(shiyongjinji)

            peiwu=html_1.xpath('//*[@id="art_text"]/div/p[position()>=15]//text()')
            peiwu_str=''.join(peiwu)

            img=html_1.xpath('//*[@id="art_text"]/div/p[1]/img/@src')
            img_url=self.part_url+img[0]
            img_url_str=self.save_img(img_url,mingcheng_str)

            desc=keming_str+'\n'+lichuang_str+'\n'+yaoxaixingzhuang_str+'\n'+shiyongjinji_str+'\n'+peiwu_str

            shuju=(mingcheng_str,bieming_str,keming_str,guijiung,yaoxing,wuwei,zhiwuxingtai_str,source_str,eff_function_str,desc,img_url_str)
            tcm = TcmDetailInfomations.objects.create(
                tcm_title=shuju[0], alias=shuju[1], family_name=shuju[2], channel_entry=shuju[3], medicinal=shuju[4],
                four_gas=shuju[4],
                five_tastes=shuju[5]
                , medicinal_part=shuju[6], source=shuju[7], efficacy_function=shuju[8], detail_desc=shuju[9]
            )
            TcmPic.objects.create(tcm_title=shuju[0], image=shuju[10], tcm_detail_info_id=tcm.id)
            print(shuju)
            # content.append(shuju)
        # return content

    def run(self):
        html_str = self.parse_url(self.start_url)
        # return  self.get_content_list(html_str)
        self.get_content_list(html_str)

from apps.video.models import  TcmVideo
class VideoSpider:

    def __init__(self,page):
        self.start_url = 'https://www.dayi.org.cn/list/16?pageNo='+page
        self.part_url = "https://www.dayi.org.cn"
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
                       }

    def parse_url(self, url):
        response = requests.get(url, headers=self.header)

        response.encoding = response.apparent_encoding
        return response.text

    def save_contont(self, dir,img_url, name,endwith):
        response = requests.get(img_url, headers=self.header)
        with open('./upload/'+dir+ name + endwith, "wb")as f1:
            f1.write(response.content)
            print("保存完成！")
        return  dir + name + endwith


    def replace_str(self,str1):
        return  str1.replace('】','')

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath('//div/a[@class="name"]/@href')
        img_list=[]
        img_list_div=html.xpath('//div/a/img/@src')
        for item in img_list_div:
            img_list.append(item)

        content_list_url = []

        for item in div_list:
             content_list_url.append(self.part_url+item)
        print(content_list_url,len(content_list_url))
        print(img_list,len(img_list))


        for  item in range(len(img_list)):
            html_1_str = self.parse_url(content_list_url[item])
            html_1 = etree.HTML(html_1_str)
            name=html_1.xpath('//*[@id="global"]//div//article//h1/text()')
            name_str=name[0]
            desc=html_1.xpath('//article/div/div[1]/div[2]/div[4]/span//text()')
            desc_str=''.join(desc)
            video=html_1.xpath('//div/video/@src')
            video_url=video[0]
            img_end=img_list[item].split('.')[-1]
            img_pic=self.save_contont('cover/',img_list[item],name_str,'.'+img_end)
            video_video=self.save_contont('video/',video_url,name_str,'.mp4')
            TcmVideo.objects.create(title=name_str,desc=desc_str,file=video_video,cover=img_pic,status=1,classification_id=7)

            print(video_video)
            print(img_pic)

            print(video_url)
            print('标题：',name_str)
            print('详细描述：', desc_str)




    def run(self):
        html_str = self.parse_url(self.start_url)
        self.get_content_list(html_str)

import  threading
def shuju(request):
     # for i in range(11,):
     lock=threading.Lock()
     # zy = Spider('46')
     # zy.run()
     # shujus = zy.run()
     # print(shujus)
     # count = 0
     lock.acquire()
     # for shuju in shujus:
     #     tcm = TcmDetailInfomations.objects.create(
     #         tcm_title=shuju[0], alias=shuju[1], family_name=shuju[2], channel_entry=shuju[3], medicinal=shuju[4],
     #         four_gas=shuju[4],
     #         five_tastes=shuju[5]
     #         , medicinal_part=shuju[6], source=shuju[7], efficacy_function=shuju[8], detail_desc=shuju[9]
     #     )
     #     TcmPic.objects.create(tcm_title=shuju[0], image=shuju[10], tcm_detail_info_id=tcm.id)
     #     print(shuju)
     #     count = count + 1

     # for i in range(14,17):
     #     video=VideoSpider(str(i))
     #     video.run()
     video = VideoSpider('154')
     video.run()

     lock.release()
     # print(count)
     return  JsonResponse(1,safe=0)













