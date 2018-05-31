import time
from Base.BaseOperate import OperateElement
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

from Base.StartAppiumServer import *
from Base.BaseRunner import ParametrizedTestCase

from PageObject.Index.IndexPage import indexpage
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Index_Test(ParametrizedTestCase):
    def test_Index(self):
        app = {}
        app['driver'] = self.driver
        app['path'] = PATH('../Yamls/Index/IndexLogin.yaml')
        print(app)
        page = indexpage(app)
        page.operate()
        self.assertTrue(page.checkPoint())
    @classmethod
    def setUp(cls):
        super(Index_Test, cls).setUpClass()
    @classmethod
    def tearDownClass(cls):
        super(Index_Test, cls).tearDownClass()