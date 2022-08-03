from .models import *
import numpy as np
import matplotlib.pyplot as plt
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse
import pprint
import base64
import io
import matplotlib
import random
import faker
matplotlib.use('Agg')


def test(request):
    print(request.headers)
    print(request.POST)
    print(request.body)
    return HttpResponse('test')

# Create your views here.


def index(request):
    # 主界面就那个列表视图, 左边显示设备, 右边显示该设备下的artifact
    # 主界面显示在线的设备后面多显示一个绿色的点
    # filter: 设备, artifact类型
    # 点击列表进入对应类型的artifact详情界面

    type_of_artifacts = [BasicInfor,
                         EvtxApplication,
                         EvtxAppxOperational,
                         EvtxGrouppolicyOperational,
                         EvtxNtfsOperational,
                         EvtxPowershellOperational,
                         EvtxSecurity,
                         EvtxStoreOperational,
                         EvtxSystem,
                         EvtxWindowsPowershell,
                         Iconcache,
                         Jumplist,
                         Lnk,
                         Prefetch,
                         RecycleBin,
                         RegistryAutorun,
                         RegistryConnDevice,
                         RegistryUsbname,
                         RegistryUserassist,
                         RegistryWireless,
                         Win10Activity,
                         Win10Packageid, ]

    index_page_items = []
    for artifact_cls in type_of_artifacts:
        index_page_items.append({
            'blog_url': 'blog_{}'.format(artifact_cls.__name__.lower()),
            'img_url': 'img/index/{}logo.png'.format(artifact_cls.__name__.lower()),
            'name': artifact_cls.__name__,
            'count': artifact_cls.objects.count(),
        })

    return render(request, 'index.html', {
        'index_page_items': index_page_items
    })


def iconcache(request):
    items = []
    for icon in Iconcache.objects.all()[:10]:
        item = model_to_dict(icon)
        item['event'] = 'Icon Cache'
        items.append(item)
    return render(request, 'activity_iconcache.html', {
        'items': items,
    })


def basicinfor(request):
    items = []
    for item in BasicInfor.objects.all()[:10]:
        item = model_to_dict(item)
        item['event'] = 'Basic Infor'
        items.append(item)
    return render(request, 'activity_basicinfor.html', {
        'items': items,
    })


def eventlog(request):
    pass


def registryautorun(request):
    pass


def item(request, event, idx):
    event_type_dict = {
        'iconcache': (Iconcache, 'item_iconcache.html'),
        'basicinfor': (BasicInfor, 'item_basicinfor.html'),
    }

    try:
        event_tuple = event_type_dict[event][0]
    except KeyError:
        return HttpResponse('event not found')
    try:
        event_instance = event_tuple.objects.get(idx=idx)
    except event_tuple.DoesNotExist:
        return HttpResponse('event not found')

    items = []
    for icon in Iconcache.objects.all()[:10]:
        item = model_to_dict(icon)
        item['event'] = 'Icon Cache'
        items.append(item)
    print(items)
    return render(request, 'item_base.html', {
        'item': model_to_dict(event_instance),
        'items': items,
    })


def piechart(request):
    labels = ['Icon Cache', 'Basic Infor', 'Registry Autorun',
              'Connected Device', 'USB Dedevice', 'Wireless Device']
    types = [Iconcache, BasicInfor, RegistryAutorun,
             RegistryConnDevice, RegistryUsbname, RegistryWireless]
    # sizes = [atf.objects.count() for atf in types]
    sizes = [172, 3, 20, 7, 34, 9]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = [0.1 for i in range(len(types))]
    explode[2] = 0

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%',
           shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    pic_IObytes = io.BytesIO()
    fig.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    # base64_str = base64.b64encode(pic_IObytes.read()).decode()
    return HttpResponse(pic_IObytes.read(), content_type='image/png')


def barchart(request):
    labels = ['Icon Cache', 'Basic Infor', 'Registry Autorun',
              'Connected Device', 'USB Dedevice', 'Wireless Device']
    types = [Iconcache, BasicInfor, RegistryAutorun,
             RegistryConnDevice, RegistryUsbname, RegistryWireless]
    # sizes = [atf.objects.count() for atf in types]
    sizes = [72, 3, 20, 7, 34, 9]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = [0.1 for i in range(len(types))]
    explode[2] = 0

    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(labels, sizes, width)
    fig.set_figwidth(20)
    fig.set_figheight(5)
    # fig.show()

    pic_IObytes = io.BytesIO()
    fig.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    # base64_str = base64.b64encode(pic_IObytes.read()).decode()
    return HttpResponse(pic_IObytes.read(), content_type='image/png')


def analysis(request):
    return render(request, 'analysis_base.html')


def about_us(request):
    return render(request, 'about_us.html')


def device_list(request):
    device_icon_dict = {
        'Windows10': 'img/device/windows10.png',
        'Windows8': 'img/device/windows8.png',
        'Windows7': 'img/device/windows7.png',
        'Windows Vista': 'img/device/windowsvista.png',
        'Windows XP': 'img/device/windowsxp.png',
        # 'Windows 2005': 'img/device/windows5.png',
        # 'Windows 2003': 'img/device/windows3.png',
        # 'Windows': 'img/device/windows1.png',
    }
    device_template = {
                "hostname": "Zhu Yongyu's PC",
                "mac_addr": '00-0C-29-84-BF-29',
                "amount": 6206,
                "24h": 130,
                "24h_isIncrease": True,
                "7d": 2356,
                "7d_isIncrease": True,
                "icon_cache": 42,
                "event_log": 6154,
                "registry": 10,
                "img_url": 'img/device/windows7.png',
                "isActive": True,
            }
    
    device_list = []
    f = faker.Faker()
    for i in range(10):
        temp = device_template.copy()
        device_type = random.choice(list(device_icon_dict.keys()))
        temp['hostname'] = f.name() + ' ' + device_type
        temp['mac_addr'] = f.mac_address()
        temp['24h'] = random.randint(0, 500)
        temp['24h_isIncrease'] = random.choice([True, False])
        temp['7d'] = random.randint(temp['24h'], 1500)
        temp['7d_isIncrease'] = random.choice([True, False])
        temp['icon_cache'] = random.randint(0, 100)
        temp['event_log'] = random.randint(100, 1000)
        temp['registry'] = random.randint(50, 100)
        temp['amount'] = random.randint(temp['icon_cache']+temp['event_log']+temp['registry'], temp['icon_cache']+temp['event_log']+temp['registry']+1000)
        temp['img_url'] = device_icon_dict[device_type]
        temp['isActive'] = random.choice([True, False])
        device_list.append(temp)
    
    return render(request, 'device_list.html', {
        'devices': device_list,
    })


def blog(request):
    artifact_name = request.path.split('/')[2]
    return render(request, 'blog/blog_{}.html'.format(artifact_name))




# MARK: detector

def detector(request):
    return render(request, 'detector.html')