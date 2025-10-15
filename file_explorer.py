# 文件管理器
user="改成 Windows 用户名"
import flask
import os
import psutil

flag=0;iplst=[];i=0
for interface, addrs in psutil.net_if_addrs().items():
    for addr in addrs:
        addr=addr.address
        if not 'fe80' in addr and addr != '::1' and addr != '127.0.0.1' and '-' not in addr:
            if ('::' in addr and '::1' not in addr) or "192." in addr:
                defaultip=addr;flag=1
            print(f'[{i}]{addr}');iplst.append(addr);i+=1

ip=input('ip: ')
port=1145;loc='D:/'

if 1<=len(ip)<=2:
    ip=iplst[int(ip)]
elif ip=='':
    if not flag:
        ip='127.0.0.1'
    else:
        ip=defaultip

htmlHead='''<!DOCTYPE html><head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/svg+xml" href='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22256%22 height=%22256%22 viewBox=%220 0 256 256%22%3E%3Cpath d=%22M207,48c11.35.07,29.02-1.54,39.44.06,2.88.44,7.33,2.72,7.59,5.94l.98-1h1v183c-2.49,3.85-4.54,7.16-9.56,7.94-8.44,1.3-22.26-.02-31.44.06.22-2.52,1.18-4.93,1.1-7.52-.06-2.09-1.1-4.38-1.1-4.98v-18c0-1.58-2.06-5.79-1-8.51h-2c-.91-17.32-8.59-28.38-25.94-32.55l-116.32-.2c-10.52,2.56-19.51,9.22-23.5,19.5-5.55,14.27-.5,36.71-2.24,52.26-10-.08-25.24,1.35-34.44-.06-4.75-.73-6.53-3.91-9.56-6.94v-103c7.49-1.94,14.85-6.94,21.67-10.83,40.61-23.14,81.13-46.71,121.04-70.96l62.62-.17,1.67-4.04h0Z%22 fill=%22%23fecb3d%22/%3E%3Cpath d=%22M207,48l-1.67,4.04-62.62.17c-39.91,24.25-80.43,47.82-121.04,70.96-6.82,3.89-14.18,8.89-21.67,10.83v-67c2.46-2.72,4.54-6.36,8.56-6.94,32.03-3.54,70.09,9.29,97-12,33.81.06,67.65-.26,101.45-.05h0Z%22 fill=%22%23fed45b%22/%3E%3Cpath d=%22M255,53l-.98,1c-.25-3.22-4.71-5.49-7.59-5.94-10.41-1.61-28.09,0-39.44-.06-33.8-.21-67.64.11-101.45.05-26.9,21.3-64.97,8.46-97,12-4.02.58-6.09,4.22-8.56,6.94V28c2.5-3.95,4.52-7.03,9.56-7.94,21.29,1.57,46.08-2.32,66.94-.07,14.67,1.58,19.34,15.71,28.99,24.01l140.03-.03c4.71.61,9.71,3.63,9.48,9.02h.02Z%22 fill=%22%23de9e01%22/%3E%3Cpath d=%22M212,205c.68,12.88-.5,26.09,0,39-55.94.42-112.06.43-168,0,1.74-15.55-3.31-37.99,2.24-52.26,3.99-10.28,12.98-16.94,23.5-19.5l116.32.2c17.35,4.17,25.03,15.22,25.94,32.56ZM77,204c-1.36,1.94-1.05,8,1.5,8h99c.73,0,3.08-3.17,2.55-4.45.06-1.04-2.05-3.55-2.55-3.55h-100.5Z%22 fill=%22%230b7cca%22/%3E%3Cpath d=%22M212,205h2c-1.06,2.71,1,6.92,1,8.5v18c0,.61,1.04,2.9,1.1,4.98.08,2.59-.89,4.99-1.1,7.52h-3c-.5-12.91.68-26.12,0-39Z%22 fill=%22%23de9e01%22/%3E%3Cpath d=%22M77,204h100.5c.5,0,2.61,2.51,2.55,3.55.53,1.28-1.82,4.45-2.55,4.45h-99c-2.55,0-2.86-6.06-1.5-8Z%22 fill=%22%23114a8b%22/%3E%3C/svg%3E'>
    <style>
    body {background-color: #F1FCF3;}
    a {color:#597A6C;font-size:26px;text-decoration:none;word-break:break-all;margin:10px}
    a:hover {color:#2B3B34;}
    p {font-size:26px;word-break:break-all;margin:10px}
    </style>
</head>
'''

app=flask.Flask(__name__)
@app.route('/files/',methods=['GET','POST'])
@app.route('/files/<path:pth>',methods=['GET','POST'])
def file(pth=''):
    if flask.request.method=='GET':
        if f'{loc}{pth}'[-1]=='/':
            pth=pth[:-1]
        if os.path.isfile(f'{loc}{pth}'):
            try:
                return flask.send_file(f'{loc}{pth}',download_name=pth.split('/')[-1])
            except Exception as e:
                return str(e)
        if pth == '':
            title='File Explorer'
        else:
            title=pth+' _File Explorer'
        html=htmlHead+'''<title>'''+title+'''</title>
<p style="font-size: 50px;">'''+title+'''</p>
<form action="." method="post" enctype="multipart/form-data">
    <input type="file" id="file" name="file" required>
    <button type="submit">上传</button>
</form><br>
<a href="../">...</a><br>'''
        try:
            dir = sorted(os.listdir(f'{loc}{pth}'))
            for i in dir:
                if os.path.isfile(f'{loc}{pth}/{i}'):
                    size=os.path.getsize(f'{loc}{pth}/{i}')
                    if size<1024:
                        size=str(size)+'B'
                    elif size<1048576:
                        size=str(round(size/1024,2))+'KB'
                    elif size<1073741824:
                        size=str(round(size/1048576,2))+'MB'
                    else:
                        size=str(round(size/1073741824,2))+'GB'
                    html+=f'<a href="{i}/">{i}</a>{size}<br>'
                else:
                    html+=f'<a href="{i}/">{i}</a><br>'
            return html
        except Exception as e:
            return str(e)
    else:
        file = flask.request.files['file']
        filename = file.filename
        file.save(os.path.join(f'{loc}{pth}', filename))
        return flask.redirect(flask.request.url)

@app.route('/')
def navigator():
    return htmlHead+f'''<title>网址导航</title>
<p style="font-size: 50px;">网址导航</p>
<p><br></p>
<a href="../files/">文件管理器</a><br><br>
<a href="../files/C/Users/{user}/Desktop/">桌面</a><br>
<a href="../files/C/Users/{user}/Pictures/Screenshots/">截屏</a><br>
<a href="../files/C/Users/{user}/Downloads/">下载</a><br>'''

if __name__ == '__main__':
    app.run(ip,port)