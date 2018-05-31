import unittest

from appium import webdriver


def appium_testcase(devicess):
    caps = {}
    caps["platformName"] = "android"
    caps["deviceName"] = devicess['deviceid']
    caps["appPackage"] = "com.tritonsfs.chaoaicai"
    caps["appActivity"] = ".main.guider.SplashActivity"
    driver = webdriver.Remote("http://127.0.0.1:"+str(devicess['port'])+"/wd/hub", caps)
    return driver
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """

    def __init__(self, methodName='runTest', param=None):
        print(methodName)
        super(ParametrizedTestCase, self).__init__(methodName)
        global devicess
        devicess = param

    @classmethod
    def setUpClass(cls):
        pass
        cls.driver = appium_testcase(devicess)
        # cls.devicesName = devicess["deviceName"]


    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_app()
        cls.driver.quit()
        pass
    def tearDown(self):
        pass

    @staticmethod
    def parametrize(testcase_klass, param=None):
        # print("---parametrize-----")
        # print(param)
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite


