from aip import AipFace

from picamera import PiCamera

import urllib.request

import RPi.GPIO as GPIO

import base64

import time

import os

import json
#onenet设备ID
deviceId = "943929137"
APIKey = "qReNZnFKG73xLV6IGDRd1zMNXiM="

#发送数据
def http_put_data(data):
    curren_time=time.asctime(time.localtime(time.time()))#获取当前时间
    url = "http://api.heclouds.com/devices/" + deviceId + '/datapoints?type=3'
    values = {
        "recog_log":data,
        "door_ctrl":{
            "value":1,
            "time":str(curren_time),
            "from":"Face_Judge"
        }
    }

    jdata = json.dumps(values).encode("utf-8")
    request = urllib.request.Request(url, jdata)
    request.add_header('api-key', APIKey)
    request.get_method = lambda: 'POST'
    request = urllib.request.urlopen(request)
    return request.read()

#获取数据
def http_get_data():
    url = "http://api.heclouds.com/devices/" + deviceId + '/datastreams?datastream_ids=door_stat'
    request = urllib.request.Request(url)
    request.add_header('api-key', APIKey)
    request.get_method = lambda: 'GET'
    request = urllib.request.urlopen(request)
    return request.read()

#百度人脸识别API账号信息

APP_ID='26207785'

API_KEY='ICq69piS6njgi2AoKEtRhoCt'

SECRET_KEY='rpXbGUjHOO0EHGVHP8gjyBGL4adB2hqS'

client=AipFace(APP_ID,API_KEY,SECRET_KEY)#创建一个客户端用以访问百度云

#图像编码方式

IMAGE_TYPE='BASE64'

camera=PiCamera()#定义一个摄像头对象

#用户组

GROUP='David'

#照相函数

def getimage():

    camera.resolution=(1024,768)#摄像界面为1024*768

    camera.start_preview()#开始摄像

    time.sleep(1)

    camera.capture('faceimage.jpg')#拍照并保存

    time.sleep(1)

#对图片的格式进行转换

def transimage():

    f=open('faceimage.jpg','rb')

    img=base64.b64encode(f.read())

    return img

#上传到百度api进行人脸检测

def go_api(image):

    result=client.search(str(image,'utf-8'),IMAGE_TYPE,GROUP);#在百度云人脸库中寻找有没有匹配的人脸

    if result['error_msg']=='SUCCESS':#如果成功了

        name=result['result']['user_list'][0]['user_id']#获取名字

        score=result['result']['user_list'][0]['score']#获取相似度

        if score>80:#如果相似度大于80

            if name=='yujie':

                print("欢迎%s !"%name)
                playmusic('/home/pi/Desktop/testsound/test1.mp3')
                time.sleep(3)

            elif name=='wqw':

                print("欢迎%s !"%name)
                playmusic('/home/pi/Desktop/testsound/test2.mp3')
                time.sleep(3)

            elif name=="dzy":

                print("欢迎%s !"%name)
                playmusic('/home/pi/Desktop/testsound/test3.mp3')
                time.sleep(3)

            else:

                print("对不起，我不认识你！")

                name='Unknow'

                return 0

        curren_time=time.asctime(time.localtime(time.time()))#获取当前时间

    #将人员出入的记录保存到Log.txt中

        f=open('Log.txt','a')
        f.write("Person: "+name+" "+"Time:"+str(curren_time)+'\n')
        f.close()
    #将该记录发送到onenet
        msg = "Person: "+name+" "+"Time:"+str(curren_time)+'\n'
        http_put_data(msg)
        return 1

    if result['error_msg']=='pic not has face':
        print('检测不到人脸')
        time.sleep(2)
        return 0
    else:
        print(str(result['error_code'])+' '+result['error_msg'])
    return 0

#playmusic
def playmusic(fileName):
    os.system('mplayer %s' %fileName)

#主函数

if __name__ =='__main__':

    while True:
        print('准备')
        getimage()#拍照
        img=transimage()#转换照片格式
        res=go_api(img)#将转换了格式的图片上传到百度云

        if(res==1):#是人脸库中的人
            state_t = http_get_data()
            state = str(state_t,encoding='utf-8').split('\"')[18][1]
            if (state==0):
                print("开门")
            else:
                playmusic('/home/pi/Desktop/testsound/test4.mp3')
        else:
            print("关门")
            print('稍等1秒进入下一次检测')
        time.sleep(1)
