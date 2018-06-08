import time
import os
from Base.OperatingYaml import readyaml
from Base.Operatingparams import Operatingparams as be
from Base.BaseOperate import OperateElement

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class PageObjects:
    def __init__(self, kwargs):
        self.driver = kwargs['driver']
        self.path = kwargs['path']
        self.isOperate = True
        self.operateElement = OperateElement(self.driver)
        test_msg = readyaml(self.path)
        self.testInfo = test_msg["testinfo"]
        self.testCase = test_msg["testcase"]
        self.testcheck = test_msg["check"]
        self.is_get = False
        self.msg = ""

    def operate(self):
        print(self.testCase)
        for item in self.testCase:
            m_s_g = self.msg + "\n" if self.msg != "" else ""
            result = self.operateElement.operate(item, self.testInfo)
            if not result["result"]:
                msg = "执行过程中失败，请检查元素是否存在" + item["element_info"] + "," + result.get("text", " ")
                if not result.get("webview", True):
                    msg = "切换到webview失败，请确定是否在webview页面"
                self.msg = m_s_g + msg
                self.testInfo[0]["msg"] = msg
                self.isOperate = False
                return False
            if item.get("is_time", "0") != "0":
                time.sleep(item["is_time"])  # 等待时间
                print("--等待下---")
            if item.get("operate_type", "0") == be.GET_VALUE or item.get("operate_type", "0") == be.GET_CONTENT_DESC:
                self.get_value.append(result["text"])
                self.is_get = True  # 对比数据
        return True

    def checkPoint(self, kwargs={}):
        result = self.check(kwargs)
        # print(self.driver.page_source)
        if result is not True and be.RE_CONNECT:
            self.msg = "用例失败重连过一次，失败原因:" + self.testInfo[0]["msg"]
            self.driver.launch_app()
            self.isOperate = True
            self.get_value = []
            self.is_get = False
            self.operate()
            result = self.check(kwargs)
            self.testInfo[0]["msg"] = self.msg

    '''
    检查点
    caseName:测试用例函数名 用作统计
    logTest： 日志记录
    devices 设备名
    contrary：相反检查点，传1表示如果检查元素存在就说明失败
    toast: 表示提示框检查点
    contrary_getval: 相反值检查点，如果对比成功，说明失败
    check_point: 自定义检查结果
    '''

    def check(self, kwargs):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""
        # 如果有重跑机制，成功后会默认把日志传进来
        # if kwargs.get("check_point", "0") != "0":
        #     return kwargs["check_point"]

        if self.isOperate:
            for item in self.testcheck:
                if kwargs.get("toast", "0") != "0":
                    resp = self.operateElement.toast(item["element_info"])
                else:
                    resp = self.operateElement.operate(item, self.testInfo)

                if kwargs.get("check", "0") == "0" and not resp["result"]:
                    m = "请检查元素" + item["element_info"] + "是否存在，" + item["info"] + " 操作是否成功"
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
                if kwargs.get("check", "0") == "contrary" and resp["result"]:
                    m = "请检查%s" % item["info"] + "是否成功"
                    self.msg = m_s_g + m
                    print(self.msg)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
                if kwargs.get("check", "0") == "contrary_getval" and self.is_get and resp["result"] in self.get_value:
                    m = "对比数据失败，当前取到到数据为:%s,历史取到数据为:%s" % resp["text"] % self.get_value
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
                if kwargs.get("check",
                              "0") == "0" and self.is_get and resp["text"] not in self.get_value:  # 历史数据和实际数据对比
                    result = False
                    m = "对比数据失败,获取历史数据为：" + ".".join(self.get_value) + ",当前获取的数据为：" + resp["text"]
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    break
        else:
            result = False
        return result