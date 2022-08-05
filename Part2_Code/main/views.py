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
                         Win10Packageid,
                         ]

artifacts_dict = {
    artifact_cls.__name__.lower(): artifact_cls for artifact_cls in type_of_artifacts
}

device_icon_dict = {
    'Windows10': 'img/device/windows10.png',
    'Windows8': 'img/device/windows8.png',
    'Windows7': 'img/device/windows7.png',
    'Windows Vista': 'img/device/windowsvista.png',
    'Windows XP': 'img/device/windowsxp.png',
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

def get_device_list():
    device_list = []
    
    for host in Host.objects.all():
        temp = device_template.copy()
        device_type = random.choice(list(device_icon_dict.keys()))
        temp['hostname'] = host.hostname
        temp['mac_addr'] = host.mac_addr
        temp['24h'] = host.last24h
        temp['24h_isIncrease'] = host.last24h_isIncrease
        temp['7d'] = host.last7d
        temp['7d_isIncrease'] = host.last7d_isIncrease
        temp['icon_cache'] = Iconcache.objects.filter(mac_addr=host.mac_addr).count()
        temp['event_log'] = Win10Activity.objects.filter(mac_addr=host.mac_addr).count()
        temp['registry'] = RegistryAutorun.objects.filter(mac_addr=host.mac_addr).count()
        temp['amount'] = temp['icon_cache']+temp['event_log']+temp['registry']
        temp['img_url'] = device_icon_dict[device_type]
        temp['isActive'] = host.isActive
        device_list.append(temp)
    return device_list

def index(request):
    # 主界面就那个列表视图, 左边显示设备, 右边显示该设备下的artifact
    # 主界面显示在线的设备后面多显示一个绿色的点
    # filter: 设备, artifact类型
    # 点击列表进入对应类型的artifact详情界面
    index_page_items = []
    for artifact_cls in type_of_artifacts:
        index_page_items.append({
            # 'blog_url': 'blog_{}'.format(artifact_cls.__name__.lower()),
            'artifact_list_url': '/artifact/{}'.format(artifact_cls.__name__.lower()),
            'img_url': 'img/index/{}logo.png'.format(artifact_cls.__name__.lower()),
            'name': artifact_cls.__name__,
            'count': artifact_cls.objects.count(),
        })

    return render(request, 'index.html', {
        'index_page_items': index_page_items,
    })


def artifact_list(request, artifact_name):
    query = request.GET
    artifact_cls = artifacts_dict[artifact_name.lower()]
    
    # query, maddr, limit
    qset = artifact_cls.objects.all()
    checked_hostnames = []
    if 'maddr' in query:
        try:
            qset = qset.filter(mac_addr__in=query['maddr'])
        except Exception:
            pass
        else:
            checked_hostnames = [h.hostname for h in Host.objects.filter(mac_addr__in=query['maddr'])]
    else:
        checked_hostnames = [h.hostname for h in Host.objects.all()]

    items = []
    for item in qset[:50 if 'limit' not in query else int(query['limit'])]:
        item = model_to_dict(item)
        item['event'] = artifact_cls.__name__
        items.append(item)
    
    device_list = get_device_list()
    
    return render(request, 'activity_base.html'.format(artifact_name), {
        'device_list': device_list,
        'type_of_artifacts': type_of_artifacts,
        'items': items,
        'checked_type': artifact_cls.__name__,
        'checked_hostnames': checked_hostnames,
        'headers': [k.replace('_', ' ').title() for k in items[0].keys()],  # TODO: here
        'img_url': 'img/index/{}logo.png'.format(artifact_name.lower()),
    })

def iconcache(request):
    items = []
    device_list = get_device_list()
    
    for icon in Iconcache.objects.all()[:10]:
        item = model_to_dict(icon)
        item['event'] = 'Icon Cache'
        items.append(item)
    return render(request, 'activity_iconcache.html', {
        'device_list': device_list,
        'type_of_artifacts': type_of_artifacts,
        'items': items,
    })


def basicinfor(request):
    items = []
    device_list = get_device_list()
    for item in BasicInfor.objects.all()[:10]:
        item = model_to_dict(item)
        item['event'] = 'Basic Infor'
        items.append(item)
    return render(request, 'activity_basicinfor.html', {
        'device_list': device_list,
        'type_of_artifacts': type_of_artifacts,
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
    sizes = [artifact_cls.objects.count() for artifact_cls in type_of_artifacts]
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


def barchart(request, mac_addr):
    labels = ['Icon Cache', 'Basic Infor', 'Registry Autorun',
              'Connected Device', 'USB Dedevice', 'Wireless Device']
    types = [Iconcache, BasicInfor, RegistryAutorun,
             RegistryConnDevice, RegistryUsbname, RegistryWireless]
    sizes = [atf.objects.filter(mac_addr=mac_addr).count() for atf in types]
    # sizes = [artifact_cls.objects.count() for artifact_cls in type_of_artifacts]
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


def analysis(request, mac_addr):
    print(mac_addr)
    types = [Iconcache, BasicInfor, RegistryAutorun,
             RegistryConnDevice, RegistryUsbname, RegistryWireless]
    heights = [
        artifact_cls.objects.filter(mac_addr=str(mac_addr)).count() for artifact_cls in types
    ]
    return render(request, 'analysis_base.html', {
        'heights': heights,
        'mac_addr': mac_addr,
    })


def about_us(request):
    return render(request, 'about_us.html')


def device_list_view(request):
    device_list = get_device_list()
    
    return render(request, 'device_list.html', {
        'devices': device_list,
    })


def blog(request):
    artifact_name = request.path.split('/')[2]
    return render(request, 'blog/blog_{}.html'.format(artifact_name), {
        'img_url': 'img/index/{}logo.png'.format(artifact_name),
    })




# MARK: detector

def detector(request):
    return render(request, 'detector.html')


def urldector(request):
    from .url.load import pre_url
    import json
    js = request.body.decode('utf-8')
    url = json.loads(js)['url']
    ret = pre_url(url)
    print(ret)
    return HttpResponse(ret)