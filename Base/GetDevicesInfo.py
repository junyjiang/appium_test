import os,subprocess


class GetDevicesInfo:
    def getPhoneInfo(self, devices):
        cmd = 'adb -s '+ devices + ' shell cat /system/build.prop'
        phone_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        result = {"release": "5.0", "model": "model2", "brand": "brand1", "device": "device1"}
        release = "ro.build.version.release="  # 版本
        model = "ro.product.model="  # 型号
        brand = "ro.product.brand="  # 品牌
        device = "ro.product.device="  # 设备名
        for lines in phone_info:
            for line in lines.split():
                temp = line.decode()
                if temp.find(release) >= 0:
                    result['release'] = temp[len(release):]
                    break
                if temp.find(model) >= 0:
                    result['model'] = temp[len(model):]
                    break
                if temp.find(brand) >= 0:
                    result['brand'] = temp[len(brand):]
                    break
                if temp.find(device) >= 0:
                    result['device'] = temp[len(device):]
                    break
        return result
    def getmaxmem(self,devices):
        cmd = 'adb -s ' + devices + ' shell cat /proc/meminfo'
        get_cmd_mem = os.popen(cmd).readlines()
        mem_total = 0
        mem_total_str = "MemTotal:"
        for line in get_cmd_mem:
            if line.find(mem_total_str) >= 0:
                mem_total = line[len(mem_total_str)+1:].replace('kB','').strip()
                break
        return int(mem_total)/1000000
    def getcpuinfo(self,devices):
        cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
        get_cmd = os.popen(cmd).readlines()
        find_str = "processor"
        int_cpu = 0
        for line in get_cmd:
            if line.find(find_str) >= 0:
                int_cpu += 1
        return str(int_cpu) + "核"

    def get_app_pix(self,devices):
        result = os.popen("adb -s " + devices + " shell wm size", "r")
        return result.readline().split("Physical size: ")[1]
if __name__ == '__main__':
    print(GetDevicesInfo().getPhoneInfo('166b6712'))
    print(GetDevicesInfo().getmaxmem('166b6712'))
    print(GetDevicesInfo().getcpuinfo('166b6712'))
    print(GetDevicesInfo().get_app_pix('166b6712'))
