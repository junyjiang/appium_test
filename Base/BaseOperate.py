import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from Base.Operatingparams import Operatingparams as EP
from selenium.webdriver.support.ui import WebDriverWait
import selenium,os

class OperateElement():
    def __init__(self, drvier=''):
        self.driver = drvier
    def findElement(self, mOperate):
        if type(mOperate) == dict:
            if mOperate.get("element_info", "0") == "0":  # 如果没有页面元素，就不检测是页面元素，可能是滑动等操作
                return {"result": True}
            t = 5#for timeout
            try:
                WebDriverWait(self.driver,t).until(lambda x: self.element_by(mOperate))
                return {"result": True}
            except selenium.common.exceptions.TimeoutException:
                return {"result": True}
            except selenium.common.exceptions.NoSuchElementException:
                print("找不到数据")
                return {"result": False}

    def operate(self, mOperate, testInfo):
        res = self.findElement(mOperate)
        if res["result"]:
            return self.operate_by(mOperate, testInfo,)
        else:
            return res
    def operate_by(self, mOperate, device):
        try:
            if mOperate.get("operate_type", "0") == "0":  # 如果没有此字段，说明没有相应操作，一般是检查点，直接判定为成功
                return {"result": True}
            elements = {
                EP.SWIPE_DOWN: lambda: self.swipeToDown(),
                EP.SWIPE_UP: lambda: self.swipeToUp(),
                EP.SWIPE_LEFT: lambda: self.swipeLeft(),
                EP.SWIPE_RIGHT: lambda: self.swipeToRight(),
                EP.CLICK: lambda: self.click(mOperate),
                EP.GET_VALUE: lambda: self.get_value(mOperate),
                EP.SET_VALUE: lambda: self.set_value(mOperate),
                EP.ADB_TAP: lambda: self.adb_tap(mOperate, device),
                EP.GET_CONTENT_DESC: lambda: self.get_content_desc(mOperate),
                EP.PRESS_KEY_CODE: lambda: self.press_key_code(mOperate)

            }
            return elements[mOperate.get("operate_type")]()
        except IndexError:
            print(mOperate["element_info"] + "索引错误")
            return {"result": False}

        except selenium.common.exceptions.NoSuchElementException:
            print(mOperate["element_info"] + "页面元素不存在或没有加载完成")

            return {"result": False}
        except selenium.common.exceptions.StaleElementReferenceException:
            print(mOperate["element_info"] + "页面元素已经变化")
            return {"result": False}
        except KeyError:
            # 如果key不存在，一般都是在自定义的page页面去处理了，这里直接返回为真
            return {"result": True}
    '''
    根据坐标进行点击
    '''
    def adb_tap(self, mOperate,devices):
        bounds = self.element_by(mOperate).location
        x = str(bounds["x"])
        y = str(bounds["y"])

        cmd = "adb -s " + devices+ " shell input tap " + x + " " + y
        print(cmd)
        os.system(cmd)
        return {"result": True}
    '''
    处理toast
    '''
    def toast(self,xpath):
        try:
            WebDriverWait(self.driver,3).until(expected_conditions.presence_of_element_located(By.XPATH,xpath))
            return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            return {"result": False}
        except selenium.common.exceptions.NoSuchElementException:
            return {"result": False}
    '''
    点击element
    '''
    def click(self,mOperate):
        if mOperate['find_type'] == EP.find_element_by_id or mOperate['find_type'] == EP.find_element_by_xpath:
            self.element_by(mOperate).click()
        elif mOperate['find_type'] == EP.find_elements_by_id:
            self.element_by(mOperate)[mOperate["index"]].click()
        return {"result": True}
    '''
    发送键盘事件
    '''
    def press_key_code(self,mOperate):
        self.driver.press_keycode(mOperate.get('code', 0))
        return {"result": True}

    def get_content_desc(self, mOperate):
        result = self.elements_by(mOperate).get_attribute("contentDescription")
        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return re_reulst

    def swipeToUp(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)
        print("执行上拉")
        return {"result": True}

    # swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000 从200滑动到400
    def swipeToDown(self):
        height = self.driver.get_window_size()["height"]
        x1 = int(self.driver.get_window_size()["width"] * 0.5)
        y1 = int(height * 0.25)
        y2 = int(height * 0.75)

        self.driver.swipe(x1, y1, x1, y2, 1000)
        # self.driver.swipe(0, 1327, 500, 900, 1000)
        print("--swipeToDown--")
        return {"result": True}

    def swipeLeft(self):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x1 = int(width * 0.75)
        y1 = int(height * 0.5)
        x2 = int(width * 0.05)
        self.driver.swipe(x1, y1, x2, y1, 600)
        return {"result": True}

    def swipeToRight(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        x1 = int(width * 0.05)
        y1 = int(height * 0.5)
        x2 = int(width * 0.75)
        self.driver.swipe(x1, y1, x1, x2, 1000)
        print("--swipeToUp--")
        return {"result": True}

    def set_value(self, mOperate):
        """
        输入值，代替过时的send_keys
        :param mOperate:
        :return:
        """
        self.element_by(mOperate).send_keys(mOperate["msg"])
        return {"result": True}

    def get_value(self, mOperate):
        '''
        读取element的值,支持webview下获取值
        :param mOperate:
        :return:
        '''

        resutl = ""
        if mOperate.get("find_type") == EP.find_element_by_id:
            element_info = self.element_by(mOperate)[mOperate["index"]]
            if mOperate.get("is_webview", "0") == 1:
                result = element_info.text
            else:
                result = element_info.get_attribute("text")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)  # 只匹配中文，大小写，字母
            return {"result": True, "text": "".join(re_reulst)}

        element_info = self.element_by(mOperate)
        if mOperate.get("is_webview", "0") == 1:
            result = element_info.text
        else:
            result = element_info.get_attribute("text")

        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return re_reulst



    def element_by(self,mOperate):
        elements = {
            EP.find_element_by_id: lambda: self.driver.find_element_by_id(mOperate['element_info']),
            EP.find_element_by_class_name: lambda: self.driver.find_element_by_class_name(mOperate['element_info']),
            EP.find_element_by_css_selector: lambda: self.driver.find_element_by_css_selector(mOperate['element_info']),
            EP.find_element_by_xpath: lambda: self.driver.find_element_by_xpath(mOperate['element_info']),
            EP.find_elements_by_id: lambda: self.driver.find_elements_by_id(mOperate['element_info'])

        }
        return elements[mOperate['find_type']]()

