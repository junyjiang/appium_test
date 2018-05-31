from Base.BaseRunner import ParametrizedTestCase
from PageObject.Pages import PageObjects


class indexpage:
    def __init__(self, kwargs):
        _init = {'driver': kwargs['driver'], 'path': kwargs['path']}
        print(_init)
        self.page = PageObjects(_init)

    def operate(self):  # 操作步骤
        self.page.operate()

    def checkPoint(self):  # 检查点
        self.page.checkPoint()

