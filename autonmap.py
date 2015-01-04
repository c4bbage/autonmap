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
            #self.ret[host]=self.portscan[host].state(),[(x,self.portscan[host]['tcp'][x]['name']) for x in self.portscan[host]['tcp'].keys()]
            # print [(x,self.portscan[host][x].keys()) for x in self.portscan[host].all_protocols()]
            # for i in x in self.portscan[host].all_protocols():
            #   print x,self.portscan[host][x]
        # return self.ret
        # for host in self.ret.keys():
        #     #print host,self.ret[host]
        #     for i in self.ret[host][1]:
        #         if(i[0]==22):
        #             print host+":"+str(22)+":ssh"+"\n"
        #         elif(i[0]==21):
        #             print host+":"+str(21)+":ftp"+"\n"
        #         elif(i[0]==80):
        #             print host+":"+str(80)+":http"+"\n"
        #         elif(i[0]==443):
        #             print host+":"+str(443)+":http"+"\n"
        #         elif(i[0]==873):
        #             print host+":"+str(i[0])+"rsync\n"
        #         elif(i[0]==1433):
        #             print host+":"+str(1433)+":mssql"+"\n"        
        #         elif(i[0]==3306):
        #             print host+":"+str(3306)+":mysql"+"\n"
        #         elif(i[0]==3389):
        #             print host+":"+str(3389)+":rdp"+"\n"
        #         elif(i[0]==8000):
        #             print host+":"+str(8000)+":http"+"\n"
        #         elif(i[0]==8080):
        #             print host+":"+str(8080)+":http"+"\n"
        #         elif(i[0]==8888):
        #             print host+":"+str(8888)+":http"+"\n"
        #         elif(i[0]==27017):
        #             print host+":"+str(27017)+":mongodb"+"\n"
        #         elif(i[0]==11211):
        #             print host+":"+str(11211)+":memcache"+"\n"
        #         else:
        #             pass
        #self.logtofile(resline)
        #print resline
        # self.ret = self.proc.stdout.readlines() 
        # if len(self.ret) == 3: 
        #     if "SUCCESS" in self.ret[2]: 
        #         self.lock.acquire() 
        #         print self.host, self.port, self.ret[2] 
        #         self.lock.release() 
        # stdmsg, errmsg = self.proc.communicate() 
        # self.timer.cancel() 
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