import unittest,time,os

import random

from Base.BaseAdb import execadb
from Base import BSTestRunner
from Base.BaseRunner import appium_testcase, ParametrizedTestCase
from Base.StartAppiumServer import StartAppiumServer
from TestCases.Index_Case import Index_Test

def runserver():
    devicesid = execadb().checkconnect()
    for deviceid in devicesid:
        port = 4724#random.randint(4724, 4800)
        bport = 4734#str(port + 10)
        StartAppiumServer().startappium(devices=deviceid, port=str(port), bport=bport)
        time.sleep(5)
        # driver = appium_testcase(port=port, deviceid=deviceid)

if __name__ == '__main__':
    runserver()
    devices = {'deviceid':'166b6712',
               'port':'4724'}
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(Index_Test, param=devices))
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Index_Test))
    now = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join('/Users/huangshaohua/appium_test/Report')
    file = os.path.join(file_dir, (now + '-result.html'))
    re_open = open(file, 'wb')
    runner = BSTestRunner.BSTestRunner(stream=re_open, title='接口测试报告', description='测试报告详情')
    basdir = os.path.abspath(os.path.dirname(__file__))
    runner.run(suite)