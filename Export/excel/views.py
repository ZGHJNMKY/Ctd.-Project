from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from openpyxl import load_workbook
import datetime
import cx_Oracle
import pandas
import codecs

# Create your views here.
def fileupload(request):
    return render(request, 'FileUpload.html', {'fuck':'Fuck'})

def upload(request):
    if request.method == 'POST':
        conn = cx_Oracle.connect('apps/apps@20.20.1.22:1551/UAT')
        cursor = conn.cursor()
        obj = request.FILES.get('upload')
        context = str(obj.name)
        extraName = context.split('.')[-1]
        if extraName != 'xlsx' and extraName != 'x' \
                                                '' \
                                                'ls':
            return render(request, 'FileUpload.html', {'context':'请上传Excel文件'})
        with open('uploads/' + str(datetime.datetime.now().year) +
                  str(datetime.datetime.now().month) + str(datetime.datetime.now().day) +
                  str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute)
                  + '.' + extraName, 'wb+') as destination:
            for chunk in obj.chunks():
                destination.write(chunk)
            wb = load_workbook(destination)
            sheetName = wb.get_sheet_names()[0]
            ws = wb.get_sheet_by_name(sheetName)
            #转换html预览
            xd = pandas.ExcelFile(destination)
            df = xd.parse()
            with codecs.open('1.html','w','utf-8') as html_file:
                html_file.write(df.to_html(header = True, index = False))
            for cells in ws.rows:
                cellValue = cells[0]
                if cellValue.row <= 2 or cellValue.row > 85:
                    continue
                sql = 'INSERT INTO CUX_BI_electricity (seq_num, elec_year,elec_month,factory_name,' \
                      'return_circui,install_site,last_mon_elec_meter ) ' \
                      'VALUES(:seq_num, :elec_year, :elec_month, :factory_name, ' \
                      ':return_circui, :install_site, :last_mon_elec_meter)'
                pramas = {'seq_num':557, 'elec_year':cells[1].value,
                          'elec_month':cells[2].value, 'factory_name':cells[3].value,
                          'return_circui':cells[4].value, 'install_site':cells[5].value,
                          'last_mon_elec_meter':cells[6].value}
                cursor.execute(sql,pramas)
                conn.commit()
    return render(request, 'FileUpload.html', {'context':obj.name + ' ' + '导入成功！'})