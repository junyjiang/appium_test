import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class execadb:

    '''
    检查是否有手机连接
    若无手机连接返回false并提示
    '''
    def checkconnect(self):
        cmd = 'adb devices'
        deviceId=[]
        deviceinfo = os.popen(cmd).readlines()
        for line in deviceinfo:
            if line.find('\tdevice')>= 0:
                deviceId.append(line.split('\tdevice')[0])
        if len(deviceId) == 0:
            print('当前无手机链接')
            return False
        return deviceId

    def initappiumapk(self,devices):
        for device in devices:
            os.popen("adb -s %s uninstall io.appium.uiautomator2.server.test" % device)
            os.popen("adb -s %s uninstall io.appium.uiautomator2.server" % device)
            os.popen("adb -s %s install -r %s" % (device, PATH("../app/appium-uiautomator2-server-v1.7.0.apk")))
if __name__=='__main__':
    # print(execadb().checkconnect())
    deviceid = execadb().checkconnect()
    print(type(deviceid))
    if type(deviceid) == list:
        execadb().initappiumapk(deviceid)
    else:
        pass