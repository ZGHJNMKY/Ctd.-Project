import os
import xlrd as xlrd
import time
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from . import models
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


logger = logging.getLogger(__name__)


# Create your views here.
def login(request):
    return render(request, 'login.html')


def loginValidate(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        password = request.POST.get("password")
        try:
            validate = models.UserInfo.objects.get(user=account).password
        except models.UserInfo.DoesNotExist:
            return HttpResponse('2')
        if password == validate:
            return HttpResponse('1')
    return HttpResponse('2')

def navi(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        logger.error(account)
        resultlist = models.authorityRecord.objects.filter(authority_by=account)
        resultlistjson = serializers.serialize("json", resultlist)
        logger.error(resultlistjson)
    return HttpResponse((resultlistjson))


def index(request):
    return render(request, 'navi.html', {'context': '上传文件'})

def homePage(request):
    return render(request, 'upload.html', {'context': '上传文件'})

# 验证文件的有效性并返回名称
def validate(request):
    if request.method == 'POST':
        obj = request.FILES.get('excel')
        fileTitle = str(obj.name)
        extraName = fileTitle.split('.')[-1]
        validateInfo = {'isValidate': True, 'context': '', 'fileName': ''}
        if extraName != 'xlsx' and extraName != 'xls':
            # return render(request, 'upload.html', {'context':'请上传Excel文件！'})
            validateInfo['isValidate'] = False
            logger.error(json.dumps(validateInfo))
            return HttpResponse(json.dumps(validateInfo))
        # 如扩展名是excel，则对文件进行重命名和转存
        fileName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + extraName
        with open('D:\\DataExport\\uploads\\' + fileName, 'wb+') as destination:
            for chunk in obj.chunks():
                destination.write(chunk)
        validateInfo['context'] = fileTitle
        validateInfo['fileName'] = fileName
        logger.error(validateInfo)
        return HttpResponse(json.dumps(validateInfo))


def upload(request):
    if request.method == 'POST':
        importby = request.POST.get("account")
        importname = request.POST.get("orignalFileName")
        importtype = request.POST.get("typeSelect")
        importdate = request.POST.get("dateinput")
        importyear = str(importdate).split('-')[0]
        importmonth = str(importdate).split('-')[1]
        logger.error(importyear)
        logger.error("importby = " + str(importby) + " importname = " + str(importname) + " importtype = " + str(importtype))
        record = models.ImportRecord()
        record.import_by = importby
        record.import_month = importmonth
        record.import_name = importname
        record.import_type = importtype
        record.import_year = importyear
        record.save()
    return HttpResponse('上传成功！')




def download(request):
    fileName = request.POST.get('fileName')
    file = open('uploads/' + '20180711133732.xls', 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="fileName"'
    return response


def home(request):
    return render(request, 'basic_table.html')


def selectRecord(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        type = request.POST.get("type")
        logger.error('account = ' + str(account) + 'type = ' + str(type))
        recordList = models.ImportRecord.objects.filter(import_by=account, import_type=type)
        paginator = Paginator(recordList, 5)
        page = request.POST.get('page', 1)
        try:
            logger.error(page)
            recordList = paginator.page(page)
        except PageNotAnInteger:
            recordList = paginator.page(1)
        except EmptyPage:
            recordList = paginator.page(paginator.num_pages)
        recordList_json = serializers.serialize("json", recordList)
        logger.error(recordList_json)
    return HttpResponse((recordList_json))

