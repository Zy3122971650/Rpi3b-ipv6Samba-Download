# python python-pip samba git aria2 you-get flask systemd-service timer文件

sudo apt update 
 
sudo apt install redis python3 python3-dev python3-pip samba samba-common-bin git aria2 

python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests redis qcloudapi-sdk-python flask you-get

#git clone webPath

#cd webPath

# 生成ddns配置文件
#DONE:1.添加启动redis的服务 2.整合ddns和redis的服务文件 ->由main.py启动redis
echo "配置systemd服务/"

echo "正在生成DDNS配置文件/generating the .service and .timer files for ddns"
echo -e "[Unit]\nDescription=ipv6 DDNS service\n[Service]\nType=simple\nUser=pi\nExecStart=python3 $PWD/src/ddns/ddns.py\n[Install]\nWantedBy=multi-user.target">ddns.service
echo -e "[Unit]\nAfter=network.target\nDescription=ipv6 DDNS service per 120s \n[Timer]\nOnUnitActiveSec=2m\nOnActiveSec=2min\nUnit=ddns.service\n[Install]\nWantedBy=multi-user.target">ddns.timer

echo -e "[Unit]\nDescription=download service\n[Service]\nType=simple\nUser=pi\nExecStart=python3 $PWD/src/main.py\n[Install]\nWantedBy=multi-user.target">RpiDownload.service

echo "正在移动文件到->/etc/systemd/system"
sudo cp $PWD/ddns.service /etc/systemd/system/
sudo cp $PWD/ddns.timer /etc/systemd/system/
sudo cp $PWD/RpiDownload.service /etc/systemd/system/



echo "配置Arira2、you-get服务"
echo -n"输入aria2下载的文件的默认储存位置，you-get也会使用同样的路径"
read path
echo "生成aria2配置文件"
echo -e "# Copy from 'http://zy-wang.github.io/2019/04/18/%E5%85%B3%E4%BA%8Earia2%E6%9C%80%E5%AE%8C%E6%95%B4%E7%9A%84%E4%B8%80%E7%AF%87/\n\n# touch /data/aria2.session\n# vim /etc/aria2/aria2.conf\n## '#'开头为注释内容, 选项都有相应的注释说明, 根据需要修改 ##\n## 被注释的选项填写的是默认值, 建议在需要修改时再取消注释  ##\n\n## 文件保存相关 ##\n\n# 文件的保存路径(可使用绝对路径或相对路径), 默认: 当前启动位置\ndir=$path\n\n# 启用磁盘缓存, 0为禁用缓存, 需1.16以上版本, 默认:16M\n#disk-cache=32M\n#disk-cache=32M\n# 文件预分配方式, 能有效降低磁盘碎片, 默认:prealloc\n# 预分配所需时间: none < falloc ? trunc < prealloc\n# falloc和trunc则需要文件系统和内核支持\n# NTFS建议使用falloc, EXT3/4建议trunc, MAC 下需要注释此项\nfile-allocation=trunc\n# 断点续传\ncontinue=true\n\n## 下载连接相关 ##\ntimeout = 60\nmax-tries = 1\n# 最大同时下载任务数, 运行时可修改, 默认:5\nmax-concurrent-downloads=10\n# 同一服务器连接数, 添加时可指定, 默认:1\nmax-connection-per-server=10\n# 最小文件分片大小, 添加时可指定, 取值范围1M -1024M, 默认:20M\n# 假定size=10M, 文件为20MiB 则使用两个来源下载; 文件为15MiB 则使用一个来源下载\nmin-split-size=10M\n# 单个任务最大线程数, 添加时可指定, 默认:5\nsplit=8\n# 整体下载速度限制, 运行时可修改, 默认:0\n#max-overall-download-limit=0\n# 单个任务下载速度限制, 默认:0\n#max-download-limit=0\n# 整体上传速度限制, 运行时可修改, 默认:0\n#max-overall-upload-limit=0\n# 单个任务上传速度限制, 默认:0\n#max-upload-limit=0\n# 禁用IPv6, 默认:false\ndisable-ipv6=false\n\n## 进度保存相关 ##\n\n# 从会话文件中读取下载任务\n#input-file=/home/zy/aria2.session\n# 在Aria2退出时保存`错误/未完成`的下载任务到会话文件\n#save-session=/home/zy/aria2.session\n# 定时保存会话, 0为退出时才保存, 需1.16.1以上版本, 默认:0\n#save-session-interval=60\n\n## RPC相关设置 ##\n\nenable-rpc=true\npause=false\nrpc-allow-origin-all=true\nrpc-listen-all=true\nrpc-save-upload-metadata=true\nrpc-secure=false\n\n# 启用RPC, 默认:false\n#enable-rpc=true\n# 允许所有来源, 默认:false\n#rpc-allow-origin-all=true\n# 允许非外部访问, 默认:false\n#rpc-listen-all=true\n# 事件轮询方式, 取值:[epoll, kqueue, port, poll, select], 不同系统默认值不同\n#event-poll=select\n# RPC监听端口, 端口被占用时可以修改, 默认:6800\nrpc-listen-port=6800\n# 设置的RPC授权令牌, v1.18.4新增功能, 取代 --rpc-user 和 --rpc-passwd 选项\n#rpc-secure=<taken>\n# 设置的RPC访问用户名, 此选项新版已废弃, 建议改用 --rpc-secret 选项\n#rpc-user=<USER>\n# 设置的RPC访问密码, 此选项新版已废弃, 建议改用 --rpc-secret 选项\n#rpc-passwd=<PASSWD>\n\n## BT/PT下载相关 ##\n\n# 当下载的是一个种子(以.torrent结尾)时, 自动开始BT任务, 默认:true\n#follow-torrent=true\n# BT监听端口, 当端口被屏蔽时使用, 默认:6881-6999\nlisten-port=51413\n# 单个种子最大连接数, 默认:55\n#bt-max-peers=55\n# 打开DHT功能, PT需要禁用, 默认:true\nenable-dht=true\n# 打开IPv6 DHT功能, PT需要禁用\n#enable-dht6=false\n# DHT网络监听端口, 默认:6881-6999\n#dht-listen-port=6881-6999\n# 本地节点查找, PT需要禁用, 默认:false\nbt-enable-lpd=true\n# 种子交换, PT需要禁用, 默认:true\nenable-peer-exchange=false\n# 每个种子限速, 对少种的PT很有用, 默认:50K\n#bt-request-peer-speed-limit=50K\n# 客户端伪装, PT需要\n#peer-id-prefix=-TR2770-\nuser-agent=Transmission/2.92\n#user-agent=netdisk;4.4.0.6;PC;PC-Windows;6.2.9200;WindowsBaiduYunGuanJia\n# 当种子的分享率达到这个数时, 自动停止做种, 0为一直做种, 默认:1.0\n\nseed-ratio=1.0\n#作种时间大于30分钟，则停止作种\nseed-time=30\n# 强制保存会话, 话即使任务已经完成, 默认:false\n# 较新的版本开启后会在任务完成后依然保留.aria2文件\n#force-save=false\n# BT校验相关, 默认:true\n#bt-hash-check-seed=true\n# 继续之前的BT任务时, 无需再次校验, 默认:false\nbt-seed-unverified=true\n# 保存磁力链接元数据为种子文件(.torrent文件), 默认:false\nbt-save-metadata=true\n#on-download-complete=/home/pi/aria2/rasp.sh" > $PWD/src/download/aria2/aria2.conf
#34行会报错，但实际运行好像没什么问题？？？？
echo "生成you-get配置文件"

echo "$path" > $PWD/src/download/you_get_download_save_file_path.txt


echo "启动DDNS服务"
sudo systemctl daemon-reload
sudo systemctl disable ddns.timer
sudo systemctl enable ddns.timer
sudo systemctl start ddns.timer
sudo systemctl start RpiDownload.service
sudo systemctl restart ddns.timer
sudo systemctl restart RpiDownload.service