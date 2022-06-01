# Raspberry-Pi-Face-ID-baidu-API
来到了大一下的信通导论课大作业了，那么浅浅实现一下小组中我人脸识别端的工作吧！
### 第一步是要准备好硬件：

- 树莓派4B（现在太贵了，年初还是600+的，等等党的大失败orz）
- CSI摄像头（插入树莓派CSI插口，蓝色塑料端朝向以太网接口）
- 一个单声道扬声器（有条件多声道也可）
- 一台电脑（和树莓派建立vnc 连接）

### 开始实现：
#### 1.先启动树莓派，建立连接

要先烧录系统，然后把TF卡查到树莓派的卡槽，把TF卡查到树莓派的卡槽，把TF卡查到树莓派的卡槽，将树莓派的卡槽用网线连到家里
的路由器。
<img width="341" alt="烧录" src="https://user-images.githubusercontent.com/94554614/171319181-2854479f-df53-4702-b683-f74b29c2008d.png">

然后用 Advanced IP Scanner 来识别路由器的连接设备树莓派的动态 IP地址
<img width="740" alt="查找IP地址" src="https://user-images.githubusercontent.com/94554614/171319246-4d2111a0-5beb-4e4d-b356-ed0eae5d1714.png">

之后为了建立VNC连接先用ssh来设置允许树莓派建立VNC访问
``` terminal
sudo raspi-config
```
<img width="495" alt="SSH连接" src="https://user-images.githubusercontent.com/94554614/171319301-d845a892-e581-4d06-8c34-f534186bc9c1.png">
< img  width = "495"  alt = "设置默认值"  src = " https://user-images.githubusercontent.com/94554614/171319309-91a229d3-6c78-4ffe-bde0-abc85edadb8e.png " >
设置完成后用VNC Viewer软件来访问树莓派桌面
<img width="513" alt="image" src="https://user-images.githubusercontent.com/94554614/171319476-767b86b0-352a-4cbc-9d2e-35393822308d.png">

#### 2.百度智能云下载人脸识别SDK
先百度智能注册账号，在人脸识别应用创建一个应用，然后创建人脸库
然后记得把自己应用的 AppID,API Key,Sec Key 记录下来，后面用。
然后建立人脸库，在上传人脸，人脸库的ID记下来。
< img 宽度= “1109”  alt = “图像”  src = “ https://user-images.githubusercontent.com/94554614/171320290-b90a1e9f-2af1-446c-94d7-6a96fc11e255.png ” >
然后去平台的HTTP SDK页面下载Python HTTP SDK
然后用VNC Viewer的上传工具传到树莓派桌面
然后在树莓派上解压
<img width="1280" alt="image" src="https://user-images.githubusercontent.com/94554614/171320694-cec313e7-df48-4492-9a2f-bedcc72d6a15.png">
#### 然后
