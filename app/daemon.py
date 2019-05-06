#! /usr/bin/python3

import json
import socket
import requests
import urllib.parse as urlparse

from bs4 import BeautifulSoup


class TCPDaemon(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 9090))
        self.sock.listen(10)

    def get_message(self, conn):
        result = b''
        while True:
            data = conn.recv(1024)
            print("Data: [{}]".format(data))
            if not data:
                break
            result += data
            print('concat data to result')
            if data.decode('utf8').endswith('\r\n'):
                break
        print('After while')
        return result.replace(b'#END#', b'')

    def get_user_card(self, url):
        print('Incoming url: {}'.format(url))
        parsed = urlparse.parse_qs(url)
        header, title = parsed.get(b'header'), parsed.get(b'title')
        form = '''<div>
            <h1>{header}</h1>
            <h2>{title}</h2>
            <img src='https://bipbap.ru/wp-content/uploads/2017/12/Stihi-pro-kotikov.-Anatolij-Movshovich-660x330.jpg' />
        </div>'''.format(header=header[0].decode('utf-8'), title=title[0].decode('utf-8'))
        return form

    '''
    def get_url_info(self, url):
        print('Incoming url: {}'.format(url))
        response = requests.get(url.strip())
        soup = BeautifulSoup(response.text, 'lxml')
        d = { 'url' : url.decode('utf8') }
        d['title'] = soup.find("meta",  property="og:title")['content']
        d['desc'] = soup.find("meta",  property="og:description")['content']
        d['image'] = soup.find("meta",  property="og:image")['content']
        return json.dumps(d)
    '''

    def loop_forever(self):
        while True:
            conn, addr = self.sock.accept()
            #conn.settimeout(5.0)
            print("Get message...")
            result = self.get_message(conn)
            print("Message conent: [{}]".format(result))
            #info = self.get_url_info(result.strip())
            info = self.get_user_card(result.strip())
            print("End get message...")
            conn.send(info.encode('utf8'))
            conn.close()


if __name__ == "__main__":
    daemon = TCPDaemon()
    daemon.loop_forever()
