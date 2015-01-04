#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# auto scan with nmap 
# c4bbage 
import nmap
import os 
import sys 
import Queue 
import threading 
host_queue = Queue.Queue(0) 
class scanopt(threading.Thread): 

    def __init__(self): 
        threading.Thread.__init__(self) 
        # self.host_queue = host_queue 
        self.timeout = 600 
        self.lock = threading.Lock() 
        self.portscan=nmap.PortScanner()  
        self.ports='21,22,23,25,80,163,443,873,1433,1434,3306,3389,6050,8000,8080,8888,27017,11211'
        self.ret={}

    def run(self): 
        while True:
            if host_queue.qsize() > 0:            
                self.host = host_queue.get()
                self.crack(self.host)
            else:
                break
        print 


    def crack(self, host): 
        self.lock.acquire()
        try:
            self.portscan.scan(hosts=host,arguments="-Pn -sV --open -p"+self.ports)
        except Exception, e:
            pass # raise e

        for host in self.portscan.all_hosts():
            for i in ([(x,self.portscan[host]['tcp'][x]['name']) for x in self.portscan[host]['tcp'].keys()]):
                print ":".join((host,str(i[0]),str(i[1])))
        self.lock.release()

if __name__=='__main__': 

    if len(sys.argv) != 3: 
        print "error" 
        sys.exit(1) 

    host_file = sys.argv[1] 
    num_works = int(sys.argv[2]) 
    #host_queue = Queue.Queue(0) 

    hosts = open(host_file, "r").readlines() 
    for host in hosts: 
        host = host.strip() 
        if host != "": 
            host_queue.put(host)
    #exit(0)

    nmap_threads = [] 
    for x in range(num_works): 
        nmap_threads.append(scanopt()) 
     
    for nmap_thread in nmap_threads: 
        nmap_thread.start() 
     
    for nmap_thread in nmap_threads: 
        nmap_thread.join()
