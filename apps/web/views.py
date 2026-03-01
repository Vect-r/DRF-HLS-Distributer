from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.master.models import *

# Create your views here.
def index(request):
    context={}
    videos = Video.objects.order_by('-created_at').all()
    paginator = Paginator(videos, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    context['page_obj']=page_obj
    context['all_tags']=Tag.objects.all()
    context['all_networks']=Network.objects.all()

    return render(request,'web/intro.html',context)


