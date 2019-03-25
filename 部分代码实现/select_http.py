'''
    使用select + 事件循环 + 回调实现http请求
'''
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from urllib.parse import urlparse
import socket

selector = DefaultSelector()
urls = ["https://www.baidu.com", "https://www.zhihu.com"]
Sign = False


class Fecth:
    def connected(self, key):
        selector.unregister(key.fd)
        self.client.send("GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection:close\r\n\r\n".format(path=self.path,host=self.host).encode('utf-8'))
        selector.register(self.client.fileno(), EVENT_READ, self.read)

    def read(self, key):
        data = self.client.recv(1024)

        if data:
            self.result += data
        else:
            selector.unregister(key.fd)
            self.result = self.result.decode("utf-8")
            self.result = self.result.split('\r\n\r\n')[1]
            print(self.result)
            self.client.close()
            urls.remove(self.spider_url)
            if not urls:
                global Sign
                Sign = True

    def get_html(self, url):
        self.spider_url = url
        self.result = b""
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        if self.path == "":
            self.path = '/'

        self.client = socket.socket()
        self.client.setblocking(False)
        try:
            self.client.connect((self.host, 80))
        except BlockingIOError as e:
            pass

        selector.register(self.client.fileno(), EVENT_WRITE, self.connected)


def loop():
    while not Sign:
        ready = selector.select()
        for key, mask in ready:
            call_back = key.data
            call_back(key)


if __name__ == "__main__":
    for url in urls:
        fetch = Fecth()
        fetch.get_html(url)
    loop()
