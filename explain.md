# 1.人脸识别部分的实现
在这里我们的思路是先用摄像头拍照片并且零时存储，然后调用百度API,将照片上传以供识别
``` Python
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
#发送到百度云进行识别
def go_api(image):

    result=client.search(str(image,'utf-8'),IMAGE_TYPE,GROUP);#在百度云人脸库中寻找有没有匹配的人脸

    if result['error_msg']=='SUCCESS':#如果成功了

        name=result['result']['user_list'][0]['user_id']#获取名字

        score=result['result']['user_list'][0]['score']#获取相似度
        ##后面就是识别成功之后的逻辑##
```
当然，我们不一定每次都能成功识别，尤其在开发阶段，所以我们要写代码接口来解读这些错误码
而同时，在正常工况下，人不在的时候识别功能也是开着的，所以必然会有识别不到的正常报错，我们要把这个和其他错误区分开来
``` Python
if result['error_msg']=='pic not has face':
        print('检测不到人脸')
        time.sleep(2)
        return 0
    else:
        print(str(result['error_code'])+' '+result['error_msg'])
    return 0
```
# 2.人脸识别成功后的逻辑
人脸识别成功后会根据小组内不同人而分别播放欢迎词，欢迎词是我事先录好的，这里使用了树莓派自带的mplayer来播放。由于在该项目进行的时候我还不是特别熟悉树莓派的系统，所以就写了一个绝对路径来播放我们的音频。
``` Python
#playmusic
def playmusic(fileName):
    os.system('mplayer %s' %fileName)
```
### 指令发送
在该工程中，我们的整个系统通过onene平台与微信小程序相连，所以我们在识别成功之后会向onenet的数据库发送人员识别成功的日志，并且发送指令1到门锁控制端。
在这里主要参考了onenet官方平台的文档
https://open.iot.10086.cn/doc/art727.html#108
接下来是使用urllib模块来发送tcp的代码
``` Python
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
```
### 在识别成功（人脸置信度达到80以上）之后的代码
播放音频并且发送消息，同时树莓派本地也要写上日志，方便开发时期的调试
``` Python
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
```
# 收尾工作
写下主函数，其中要注意，由于我们的项目具有其他打开门的方式，所以会有传感器模块来向onenet的数据集传输门的开关状态，我们的门禁系统要在不同的状态下做出不同的反应
所以要有一个获取状态的方式
``` Python
#获取数据
def http_get_data():
    url = "http://api.heclouds.com/devices/" + deviceId + '/datastreams?datastream_ids=door_stat'
    request = urllib.request.Request(url)
    request.add_header('api-key', APIKey)
    request.get_method = lambda: 'GET'
    request = urllib.request.urlopen(request)
    return request.read()
```
主函数就是写一个循环，不断地拍照，覆盖式保存，发送识别，获取状态，最好在不同状态下print出对应状态，方便后期在树莓派端的调试工作
``` Python
#主函数

if __name__ =='__main__':

    while True:
        print('准备')
        getimage()#拍照
        img=transimage()#转换照片格式
        res=go_api(img)#将转换了格式的图片上传到百度云
        state_t = http_get_data()
        state = str(state_t,encoding='utf-8').split('\"')[18][1]
        if(res==1 and state=='0'):#是人脸库中的人
                print("开门")
        elif(res==1):
                playmusic('/home/pi/Desktop/testsound/test4.mp3')
        else:
            print("关门")
            print('稍等1秒进入下一次检测')
        time.sleep(1)
```
