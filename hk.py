
import json
from urllib.request import urlretrieve
import requests
import os
import base64
import json
from time import localtime
import time
from datetime import datetime
import shutil

#程序开始运行时间
start_time_str = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

timestr = time.strftime("%Y%m%d%H%M%S")
timestr = "hk"+timestr
html_file_name1 = timestr+"/hk1"+timestr+".html" #每次上传使用时间戳目录 timestr，方便后续一次性删除
html_file_name2 = timestr+"/hk2"+timestr+".html" #每次上传使用时间戳目录 timestr，方便后续一次性删除
html_file_name3 = timestr+"/hk3"+timestr+".html" 
html_file_name4 = timestr+"/hk4"+timestr+".html"
html_file_name5 = timestr+"/hk5"+timestr+".html"
html_file_name_arr = [html_file_name1, html_file_name2,html_file_name3, html_file_name4, html_file_name5]

data_json_name1 = timestr+"/hk1"+timestr+".json"
data_json_name2 = timestr+"/hk2"+timestr+".json"
data_json_name3 = timestr+"/hk3"+timestr+".json"
data_json_name4 = timestr+"/hk4"+timestr+".json"
data_json_name5 = timestr+"/hk5"+timestr+".json"

html_file_name_jianming = "lb简明版hk.html"
html_file_name_old1 = ""
data_json_name_old1 = ""
html_file_name_old2 = ""
data_json_name_old2 = ""
html_file_name_old3 = ""
data_json_name_old3 = ""
html_file_name_old4 = ""
data_json_name_old4 = ""
html_file_name_old5 = ""
data_json_name_old5 = ""

uploaded_image_arr = []


def get_access_token():
    data = {
        'grant_type': 'password',
        'username': '',
        'password': '',
        'client_id': 'c47c19c580caec8604c88390a1877dba0316a302d136c02fb5ad37c841f84ba3',
        'client_secret': '2bb1ca34f0406fd91fccb95b318a964c48bc1af18923164f5d63635cd0a81c74',
        'scope': 'projects user_info issues notes',
    }
    try:
        res = requests.post('https://gitee.com/oauth/token', data=data)
        res = json.loads(res.text)
        #获取access_token
        access_token = res['access_token']
    except KeyError:
        print("获取access_token失败")
        print(res.text)
        access_token = ""
    return access_token


def refresh_token(refresh_token):
    try:
        res = requests.post(
            'https://gitee.com/oauth/token?grant_type=refresh_token&refresh_token={}'.format(refresh_token))
        res = json.loads(res.text)
        #获取access_token
        access_token = res['access_token']
        print("获取到access_token： "+access_token)
    except KeyError:
        print("获取access_token失败")
        print(res.text)
    return access_token


gitee_token = get_access_token()
# gitee_token = "63b0581c1e5c046849bf79c06d76f66e"
if gitee_token == "":
   gitee_token = refresh_token(
       "decd5e264c42d59b8275f746331214f16f25a5e28be6b4a1ca0f0ce2557bd9d4")
gitee_url = "https://gitee.com/api/v5/repos/yjl1987/qinglanjiaoyu/contents/"
gitee_headers = {"access_token": gitee_token,
                 'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
                 }

qishu = ''
# 保存data_json_name_old和html_file_name_old
with open('hk_history.txt', 'r') as f1:
    s = f1.read()
    s1 = s.split(",")
    html_file_name_old1 = s1[0]
    data_json_name_old1 = s1[1]
    html_file_name_old2 = s1[2]
    data_json_name_old2 = s1[3]
    html_file_name_old3 = s1[4]
    data_json_name_old3 = s1[5]
    html_file_name_old4 = s1[6]
    data_json_name_old4 = s1[7]
    html_file_name_old5 = s1[8]
    data_json_name_old5 = s1[9]
    s = int(s1[10])
    s = s + 1
    qishu = str(s)

GitHub_url = "https://api.github.com/repos/765766546/qinglanjiaoyu/contents/"
headers = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}
IMAGE_URL = "https://tk.sycccf.com:4949/col/"+qishu

file_object = open("需要发给老爸的图hk.txt", 'r')  # 创建一个文件对象，也是一个可迭代对象
try:
    # imageNameArr_aomen = file_object.read()  # 结果为str类型
    imageNameArr_aomen = file_object.readlines()
    print(type(imageNameArr_aomen))
    print("imageNameArr_aomen=", imageNameArr_aomen)
finally:
    file_object.close()


def request_download():
    if os.path.exists("./hkimage"):
        shutil.rmtree("./hkimage", ignore_errors=True)
    os.mkdir('./hkimage')
    # os.remove(data_json_name_old)  # 这个可以删除单个文件，不能删除文件夹
    for index, name in enumerate(imageNameArr_aomen):
        # for name in imageNameArr_aomen:
        name = name.replace('\n', '')
        # time.sleep(2)
        i = index+1
        url = IMAGE_URL+name
        print("==================正在下载第【"+str(i)+"】张图片=================")
        print("==================图片地址是【"+url+"】=================")
        try:
            r = requests.get(IMAGE_URL+name, headers=headers, timeout=3)
        except Exception:
            print("==================正在下载第【"+str(i) +
                  "】张图片【"+name+"】，下载失败=================")
            continue

        with open('./hkimage'+name, 'wb') as f1:
            f1.write(r.content)

    print('==================所有图片下载完成！=================')


# 读取文件
def open_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

 # 将文件转换为base64编码，上传文件必须将文件以base64格式上传


def file_base64(data):
    data_b64 = base64.b64encode(data).decode('utf-8')
    return data_b64


def get_all_file_sha(file_path):
    url = gitee_url + file_path
    req = requests.get(url=url, headers=gitee_headers)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    if req.status_code == 200:
        print("==================获取文件【"+file_path+"】信息成功=================")
    else:
        print("==================获取文件【"+file_path+"】信息失败=================")
        print(req.text)
    return re_data


def delete_file(sha, file_path):
    url = gitee_url + file_path
    data = {
        "message": "删除",
        "sha": sha,
        "access_token": gitee_token
    }
    req = requests.delete(url=url, json=data)
    if req.status_code == 200:
        print("==================文件【"+file_path+"】删除成功=================")
    else:
        print("==================文件【"+file_path+"】删除失败=================")
        print(req.text)

 # 上传文件


def upload_file(file_data, file_path, uploaded_image_arr, filepath):
    url = gitee_url + file_path
    content = file_base64(file_data)
    data = {
        "message": "新建",
        "content": content,
        "access_token": gitee_token
    }
    req = requests.post(url=url, json=data)
    if req.status_code == 201:
        uploaded_image_arr.append(filepath)
        print("==================文件【"+file_path+"】上傳成功=================")
    else:
        print("==================文件【"+file_path+"】上傳失败，原因： "+req.text)

# 重新部署


def rebuild():
    url = "https://gitee.com/yjl1987/qinglanjiaoyu/pages/rebuild"
    data = {
        "branch": "master",
        "build_directory": "",
        "force_https": False,
        "auto_update": True,
        "access_token": gitee_token
    }
    req = requests.post(url=url, json=data)
    if req.status_code == 201:
        print("==================重新部署成功=================")
    else:
        print("==================重新部署失败================")


def delete_files(file_arr):
    for index, item in enumerate(file_arr):
        time.sleep(2)
        i = index+1
        path = item['path']
        print("==================正在删除第【"+str(i) +
              "】张图片【"+path+"】================")
        delete_file(item['sha'], path)


def today_is_week():
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    return week


def doDelete():
    # 先删除Gitee上之前上传的文件
    file_name = 'image'
    file_arr = get_all_file_sha(file_name)
    if [] != file_arr:
        delete_files(file_arr)
    file_arr = get_all_file_sha(data_json_name_old1)
    if [] != file_arr:
        delete_file(file_arr['sha'], data_json_name_old1)
    file_arr = get_all_file_sha(html_file_name_old1)
    if [] != file_arr:
        delete_file(file_arr['sha'], html_file_name_old1)
    file_arr = get_all_file_sha(data_json_name_old2)
    if [] != file_arr:
        delete_file(file_arr['sha'], data_json_name_old2)
    file_arr = get_all_file_sha(html_file_name_old2)
    if [] != file_arr:
        delete_file(file_arr['sha'], html_file_name_old2)
    file_arr = get_all_file_sha(data_json_name_old3)
    if [] != file_arr:
        delete_file(file_arr['sha'], data_json_name_old3)
    file_arr = get_all_file_sha(html_file_name_old3)
    if [] != file_arr:
        delete_file(file_arr['sha'], html_file_name_old3)
    file_arr = get_all_file_sha(data_json_name_old4)
    if [] != file_arr:
        delete_file(file_arr['sha'], data_json_name_old4)
    file_arr = get_all_file_sha(html_file_name_old4)
    if [] != file_arr:
        delete_file(file_arr['sha'], html_file_name_old4)
    file_arr = get_all_file_sha(data_json_name_old5)
    if [] != file_arr:
        delete_file(file_arr['sha'], data_json_name_old5)
    file_arr = get_all_file_sha(html_file_name_old5)
    if [] != file_arr:
        delete_file(file_arr['sha'], html_file_name_old5)
    print("==================所有文件全部删除完成！=================")


def uploadImg():
    #再上传新的图片
    image_path = "./hkimage"
    image_upload_path = timestr+"/" #每次上传使用时间戳目录 timestr，方便后续一次性删除
    for dirpath, dirnames, filenames in os.walk(image_path):
        for index, filepath in enumerate(filenames):
            i = index+1
            img_path = os.path.join(dirpath, filepath)
            size = os.path.getsize(img_path)
            if size > 10240:    # 判断文件大小，小于10kb的文件不要
                time.sleep(2)
                fdata = open_file(img_path)
                uploadpath = image_upload_path+filepath
                # uploaded_image_arr.append(uploadpath)
                # uploaded_image_arr.append(filepath)
                print("==================正在上传第【"+str(i) +
                      "】张图片【"+uploadpath+"】================")
                upload_file(fdata, uploadpath, uploaded_image_arr, filepath)
        print("==================所有图片都上傳成功！=================")


def createDataJson():
    print("==================uploaded_image_arr大小为：【" +
          str(len(uploaded_image_arr))+"】=================")
    with open(data_json_name1, 'w', encoding='utf-8') as f:
        load_dict = {"ImgList": []}
        load_dict["ImgList"] = uploaded_image_arr[0:60]
        # 生成最新的datajson文件
        json.dump(load_dict, f, indent=4, ensure_ascii=False)

    with open(data_json_name2, 'w', encoding='utf-8') as f:
        load_dict = {"ImgList": []}
        load_dict["ImgList"] = uploaded_image_arr[60:120]
        # 生成最新的datajson文件
        json.dump(load_dict, f, indent=4, ensure_ascii=False)

    with open(data_json_name3, 'w', encoding='utf-8') as f:
        load_dict = {"ImgList": []}
        load_dict["ImgList"] = uploaded_image_arr[120:180]
        # 生成最新的datajson文件
        json.dump(load_dict, f, indent=4, ensure_ascii=False)

    with open(data_json_name4, 'w', encoding='utf-8') as f:
        load_dict = {"ImgList": []}
        load_dict["ImgList"] = uploaded_image_arr[180:240]
        # 生成最新的datajson文件
        json.dump(load_dict, f, indent=4, ensure_ascii=False)

    with open(data_json_name5, 'w', encoding='utf-8') as f:
        load_dict = {"ImgList": []}
        load_dict["ImgList"] = uploaded_image_arr[240:]
        # 生成最新的datajson文件
        json.dump(load_dict, f, indent=4, ensure_ascii=False)


def uploadDataJson():
    # 上传datajson文件
    fdata = open_file(data_json_name1)
    upload_file(fdata, data_json_name1)
    print("=================="+data_json_name1+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(data_json_name2)
    upload_file(fdata, data_json_name2)
    print("=================="+data_json_name2+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(data_json_name3)
    upload_file(fdata, data_json_name3)
    print("=================="+data_json_name3+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(data_json_name4)
    upload_file(fdata, data_json_name4)
    print("=================="+data_json_name4+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(data_json_name5)
    upload_file(fdata, data_json_name5)
    print("=================="+data_json_name5+"上傳成功 == == == == == == == ===")


def creatHtmlFile():
    # 修改html文件，并生成最新的html文件
    old_str = 'var datajson="";\n'
    new_str1 = 'var datajson=\"'+data_json_name1+'\";\n'
    new_str2 = 'var datajson=\"'+data_json_name2+'\";\n'
    new_str3 = 'var datajson=\"'+data_json_name3+'\";\n'
    new_str4 = 'var datajson=\"'+data_json_name4+'\";\n'
    new_str5 = 'var datajson=\"'+data_json_name5+'\";\n'
    with open(html_file_name_jianming, "r", encoding="utf-8") as f, open(html_file_name1, "w", encoding="utf-8") as f1, open(html_file_name2, "w", encoding="utf-8") as f2, open(html_file_name3, "w", encoding="utf-8") as f3, open(html_file_name4, "w", encoding="utf-8") as f4, open(html_file_name5, "w", encoding="utf-8") as f5:
        for line in f:
            if old_str in line:
                line1 = line.replace(old_str, new_str1)
                line2 = line.replace(old_str, new_str2)
                line3 = line.replace(old_str, new_str3)
                line4 = line.replace(old_str, new_str4)
                line5 = line.replace(old_str, new_str5)
                f1.write(line1)
                f2.write(line2)
                f3.write(line3)
                f4.write(line4)
                f5.write(line5)
            elif "qishu" in line:
                line = line.replace("qishu", qishu)
                line1 = line.replace("fenshu", "1")
                line2 = line.replace("fenshu", "2")
                line3 = line.replace("fenshu", "3")
                line4 = line.replace("fenshu", "4")
                line5 = line.replace("fenshu", "5")
                f1.write(line1)
                f2.write(line2)
                f3.write(line3)
                f4.write(line4)
                f5.write(line5)
            else:
                f1.write(line)
                f2.write(line)
                f3.write(line)
                f4.write(line)
                f5.write(line)
    # os.remove(html_file_name_old5)
    # os.rename("%s.bak" % html_file_name_old5, html_file_name5)


def uploadHtmlFile():
    # 上传html文件
    fdata = open_file(html_file_name1)
    upload_file(fdata, html_file_name1)
    print("=================="+html_file_name1+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(html_file_name2)
    upload_file(fdata, html_file_name2)
    print("=================="+html_file_name2+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(html_file_name3)
    upload_file(fdata, html_file_name3)
    print("=================="+html_file_name3+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(html_file_name4)
    upload_file(fdata, html_file_name4)
    print("=================="+html_file_name4+"上傳成功 == == == == == == == ===")
    time.sleep(2)
    fdata = open_file(html_file_name5)
    upload_file(fdata, html_file_name5)
    print("=================="+html_file_name5+"上傳成功 == == == == == == == ===")


def send_message(access_token, title, description, html_file_name, imgUrl):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(
        access_token)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data1 = {
        "touser": "QingLan|heroyang",
        # "toparty": "1",
        "msgtype": "news",
        "agentid": "1000002",
        "news": {
            "articles": [
                {
                    "title": title,
                    # "description": title+"，更新时间："+end_time_str+"，开始时间："+start_time_str+",结束时间："+end_time_str,
                    "description": description,
                    "url": "https://yjl1987.gitee.io/qinglanjiaoyu/"+html_file_name,
                    "picurl": imgUrl,
                }
            ]
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    response = requests.post(url, headers=headers, json=data1).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


def get_access_token():
    # appId
    app_id = "ww25e29cc71cb7956f"
    # appSecret
    app_secret = "jm7ckxbNykKdDKIeW0f_DiYLN7WZvrQ8vr975HZHq8s"
    # post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
    #             .format(app_id, app_secret))
    post_url = (
        "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(app_id, app_secret))
    try:
        access_token = requests.get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
    # print(access_token)
    return access_token

def createDir(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath, ignore_errors=True)
    os.mkdir(dirpath)

#下载所有图片
request_download()

# doDelete()


createDir(timestr)

uploadImg()

createDataJson()

uploadDataJson()

creatHtmlFile()

uploadHtmlFile()

# 保存data_json_name_old和html_file_name_old
with open('hk_history.txt', 'w') as f1:
    f1.write(html_file_name1+","+data_json_name1 + ","+html_file_name2 +
             ","+data_json_name2+","+html_file_name3+","+data_json_name3+","+html_file_name4+","+data_json_name4+","+html_file_name5+","+data_json_name5+","+qishu)

#发送消息
#获取accessToken
accessToken = get_access_token()
week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
year = localtime().tm_year
month = localtime().tm_mon
day = localtime().tm_mday
today = datetime.date(datetime(year=year, month=month, day=day))
week = week_list[today.isoweekday() % 7]
title = "香港第"+qishu+"期,💰第"
date1 = "{} {}".format(today, week)
description = '''
    🌈共{}张图片
    💪今晚必中！
    '''
shengyushuliang = len(uploaded_image_arr)-180
# aomenImgUrl = "https://s1.ax1x.com/2023/01/03/pSiMmlV.png"
# hkImgUrl = "https://s1.ax1x.com/2023/01/05/pSkEXKe.png"
aomenImgUrl = "https://yjl1987.gitee.io/qinglanjiaoyu/%E6%BE%B3%E9%97%A8%E8%B5%84%E6%96%99icon.png"
hkImgUrl = "https://yjl1987.gitee.io/qinglanjiaoyu/%E9%A6%99%E6%B8%AF%E8%B5%84%E6%96%99icon.png"
for i in range(1, 6):
    title1 = title+str(i)+"份资料"
    if i == 5:
        description1 = description.format(shengyushuliang)
    else:
        description1 = description.format(60)
    send_message(accessToken, title1, description1,
                 html_file_name_arr[i-1], hkImgUrl)
    time.sleep(2)

time.sleep(2)
#程序结束运行时间
end_time_str = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
send_message(accessToken, "香港资料第"+qishu + "期", "开始时间：" +
             start_time_str+"，结束时间："+end_time_str, "", hkImgUrl)
os.system("pause")
