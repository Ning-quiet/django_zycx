# coding=utf-8
import requests
import os
import time
from lxml import etree
import pymysql
import django
import json

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
        for div in div_list:
             content_list_url.append(self.part_url+div.xpath("./a/@href")[0])
        for part_url in content_list_url[:2]:
            content_str=self.parse_url(part_url)
            html_1=etree.HTML(content_str)
            #中药名称
            tcm_title=html_1.xpath("//div/span[@class='name']/text()")[0]
            print('名称：'+tcm_title)

            desc_tail=html_1.xpath("//div/p[@class='intro']//text()")
            desc_tail_str= desc_tail[0] if len(desc_tail)>0 else ''
            print('详细表述：',desc_tail_str)
            #作用leibie
            func_cata=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[2]/div/div[2]//text()")
            func_cata_str=func_cata[0] if len(func_cata)>0 else ''
            print("作用",func_cata_str)
            zuzhi_func=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[3]/div/div[2]/p//text()")
            zuzhi_func_str=zuzhi_func[0] if len(zuzhi_func)>0 else ""
            print('主治',zuzhi_func_str)
            # yongfayongmliang=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[4]/div/div[2]/text()")
            # yongfayongmliang_str= yongfayongmliang[0] if len(yongfayongmliang)>0 else ''
            # print('用法用量',yongfayongmliang)
            # zhuyi=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[1]/div[7]/div/div[2]/text()")
            # zhuyi_str=zhuyi[0] if len(zhuyi)>0 else ""
            # print('注意事项',zhuyi)
            linchuang=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/article/div/div[3]/section[2]/div[2]/div/div[2]//text()")
            linchuang_str=linchuang[0] if len(linchuang)>0 else ''
            print('临床应用',linchuang)
            source=html_1.xpath('//*[@id="global"]/div[2]/div/div[2]/article/div/div[3]/section[5]/div[4]/div/div[2]/text()')
            source_str=source[0] if len(source)>0 else ''
            print('分布区域',source)

            img=html_1.xpath("//*[@id='global']/div[2]/div/div[2]/aside/div[1]/img/@src")
            img_url=img[0].split('?')[0]
            print(img_url)
            image=self.save_img(img_url,tcm_title)





    def run(self):
        html_str=self.parse_url(self.start_url)
        self.get_content_list(html_str)





if __name__=="__main__":
    zy=ZySpider("1")
    zy.run()
    # str="https://image.dayi.org.cn/public/uploads/20200317/c6deeb652e9be2a271c16b3a23203507.png?x-oss-process=image/resize,w_295"
    # img=str.split('?')
    # print(img[0])

