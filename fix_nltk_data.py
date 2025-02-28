import nltk
import shutil
import os
import socket

# 增加超时时间
socket.setdefaulttimeout(60)

# 找到 NLTK 数据目录
nltk_data_dir = nltk.data.path[0]

# 删除 tokenizers 目录
tokenizers_dir = os.path.join(nltk_data_dir, 'tokenizers')
if os.path.exists(tokenizers_dir):
    shutil.rmtree(tokenizers_dir)

# 重新下载 punkt 数据
nltk.download('punkt')
