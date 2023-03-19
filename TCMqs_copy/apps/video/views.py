from django.shortcuts import get_object_or_404
from  .models import  TcmVideo,TcmVideoClassification
from django.views import generic
from  utlis.helper import get_page_list


class TcmClassIndexView(generic.ListView):
    model = TcmVideo
    template_name = 'video/video_index.html'
    context_object_name = 'video_list'
    paginate_by = 8
    c = None
    q=None
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TcmClassIndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['c'] = self.c
        context['q'] = self.q
        classification_list = TcmVideoClassification.objects.filter(status=1).values()
        context['classification_list'] = classification_list
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        if self.c:
            classification = get_object_or_404(TcmVideoClassification, pk=self.c)
            return classification.tcmvideo_set.all().order_by('-create_time')
        else:
            self.q = self.request.GET.get("q", None)
            if self.q:
                return TcmVideo.objects.filter(title__contains=self.q).filter(status=1).order_by('-create_time')

            return TcmVideo.objects.filter(status=1).order_by('-create_time')


class VideoDetailView(generic.DetailView):
    model = TcmVideo
    template_name = 'video/detail.html'
    context_object_name = 'video'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_view_count()  # 调用自增函数
        return obj
    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        recommend_list = TcmVideo.objects.get_recommend_list()
        context['recommend_list'] = recommend_list
        return context