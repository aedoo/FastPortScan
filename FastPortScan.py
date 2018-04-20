#coding:utf-8
#powered by aedoo
#github: https://github.com/aedoo/FastPortScan

import socket
import threading,Queue
import sys
import ipaddr
import time

Port = (80,81,88,90,91,8000,8001,8080,8081,8888,9090,9000,9001,9090)   #此处放置端口列表

class PortScan(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        while True:
            if self._queue.empty():
                break
            try:

                ip = str(self._queue.get(timeout=0.5))
                for port in Port:
                    addr = (ip, port)
                    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    try:
                        s.settimeout(0.3)   
                        s.connect(addr)
                        sys.stdout.write('%s:%d\n'%(ip,port))
                    except:
                        s.close()
                        continue
            except:
                continue
def main():

    threads = []
    thread_count = 200        #线程数
    queue = Queue.Queue()
    IPduan = raw_input()      #接收输入IP段
    IPs = ipaddr.IPNetwork(IPduan)

    for ip in IPs:
        queue.put(ip)

    for i in xrange(thread_count):
        threads.append(PortScan(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    time_start = time.time()
    main()
    print 'Running Time:'+ str(time.time()-time_start)