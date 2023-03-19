import smtplib

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mass_mail, send_mail
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import *
from django.utils.html import strip_tags
from django.views.generic import View


def get_page_list(paginator, page):

    """
    分页逻辑
    if 页数>=5:
        当前页<=5时，起始页为1
        当前页>(总页数-5)时，起始页为(总页数-9)
        其他情况 起始页为(当前页-5)
    """

    page_list = []
    if paginator.num_pages > 6:
        if page.number <= 2:
            start_page = 1
        elif page.number > paginator.num_pages - 4:
            start_page = paginator.num_pages - 3
        else:
            start_page = page.number -1

        for i in range(start_page, start_page + 4):
            page_list.append(i)
    else:
        for i in range(1, paginator.num_pages + 1):
            page_list.append(i)

    return page_list






