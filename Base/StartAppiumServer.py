import socket,platform,threading,os,subprocess
import urllib.request
from urllib.error import URLError
from multiprocessing import Process

import time


class StartAppiumServer:

    '''
    判断端口是否可用
    '''
    def checkport(self, devices, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(devices, port)
            s.shutdown(2)
            print('port %s is used' %port)
            self.stop_appium(port)
            return False
        except:
            print('port %s is available' %port)
            return True
    '''
    启动Appium Server
    判断启动是否成功
    '''
    def startappium(self, devices, port,bport):
        self.stop_appium(port)
        cmd = 'appium --session-override  -p %s -bp %s -U %s' %(port ,bport, devices)
        if platform.system() == 'Windows':
            t = RunServer(cmd)
            p = Process.start(t.start())
            p.start()
            while True:
                print('windows appium server will be start')
                url = '127.0.0.1:'+ port + 'wd/hub/' + 'status'
                if self.win_runner(url):
                    print('windows appium server is running sucess')
                    break
        else:
            appium = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                          close_fds=True)
            while True:
                appium_lines = appium.stdout.readline().strip().decode()
                if 'listener started' in appium_lines or 'Error: listen' in appium_lines:
                    print('OS X appium server is running sucess')
                    break

    def stop_appium(self, port):
        if platform.system() == 'Windows':
            os.popen('taskkill /f /im node.exe')
            print('stop windows appium server now')
        else:
            cmd = 'lsof -i :{0}'.format(port)
            plist = os.popen(cmd).readlines()
            if plist:
                plisttmp = plist[1].split("    ")
                plists = plisttmp[1].split(" ")
                os.popen('kill -9 {0}'.format(plists[0]))
                print('stop OS X appium server now')
            else:
                pass

    def win_runner(self, url):
        res = None
        try:
            res = urllib.request.urlopen(url, timeout= 10)
            if str(res.getcode()).startswith('2'):
                return True
            else:
                return False
        except URLError:
            return False
        finally:
            if res:
                res.close()


class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
    def run(self):
        os.system(self.cmd)

if __name__ == '__main__':
    StartAppiumServer().startappium(devices='166b6712',port='4724',bport='4734')
    StartAppiumServer().stop_appium(port='4724')
