from  celery import  Celery
from django.conf import settings
from  django.core.mail import  send_mail
from time import  sleep
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TCMqs.settings')
django.setup()

app=Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/1')
@app.task
def send_register_email(to_email,token):
    # 发送邮件o
    subject = "中药数字化查询信息系统欢迎信息"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s欢迎您成为中药数字化查询信息系统的用户</h1>请点击下面链接激活你的账户</br><h3>十分钟内有效</h3></br>' \
                   '<a href=http://4e9f10f.r2.cpolar.cn/user/active/%s>http://4e9f10f.r2.cpolar.cn/user/active/%s</a>' % (
                   to_email, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
#celery -A celery_task.tasks worker -l info


