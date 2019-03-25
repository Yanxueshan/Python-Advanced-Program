'''
    使用socket模拟http请求（非阻塞IO）
'''

import socket
from urllib.parse import urlparse


def get_html(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = '/'

    client = socket.socket()
    client.setblocking(False)
    try:
        client.connect((host, 80))
    except BlockingIOError as e:
        pass
    
    while True:
        try:
            client.send("GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection:close\r\n\r\n".format(path=path, host=host).encode('utf-8'))
            break
        except OSError as e:
            continue

    result = b""
    while True:
        # 等待数据返回
        try:
            data = client.recv(1024)
        except BlockingIOError as e:
            continue

        if data:
            result += data
        else:
            break

    result = result.decode("utf-8")
    result = result.split('\r\n\r\n')[1]
    print(result)
    client.close()


if __name__ == "__main__":
    get_html("https://www.baidu.com")
