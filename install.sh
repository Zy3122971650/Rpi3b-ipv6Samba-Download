# python python-pip samba git aria2 you-get flask systemd-service timer文件

sudo apt update 
 
sudo apt install redis python3 python3-dev python3-pip samba samba-common-bin git aria2 nginx 

python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple redis qcloudapi-sdk-python flask you-get

#git clone webPath

#cd webPath

# 生成ddns配置文件
#TODO:1.添加启动redis的服务 2.整合ddns和redis的服务文件
echo "配置ddns的systemd服务"
echo "正在生成配置文件"
echo -e "[Unit]\nDescription=ipv6 DDNS service\n[Service]\nType=simple\nUser=pi\nExecStart=python3 $PWD/ddns.py\n[Install]\nWantedBy=multi-user.target">ddns.service

echo -e "[Unit]\nAfter=network.target\nDescription=ipv6 DDNS service per 120s \n[Timer]\nOnUnitActiveSec=2m\nOnActiveSec=2min\nUnit=ddns.service\n[Install]\nWantedBy=multi-user.target">ddns.timer

echo "正在移动文件到->/etc/systemd/system"
sudo cp $PWD/ddns.service /etc/systemd/system/
sudo cp $PWD/ddns.timer /etc/systemd/system/

echo "启动DDNS服务"
sudo systemctl daemon-reload
sudo systemctl enable ddns.timer
sudo systemctl start ddns.timer