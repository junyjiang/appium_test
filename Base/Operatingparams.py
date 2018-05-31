class Operatingparams(object):
    #定位方法
    find_element_by_id = 'id'
    find_elements_by_id = 'ids'
    INDEX = 'index'
    find_element_by_xpath = 'xpath'
    find_element_by_xpaths = 'xpaths'
    find_element_by_class_name = 'class_name'
    find_element_by_css_selector = 'css'

    #操作以及校验
    CLICK = 'click'
    ADB_TAP = 'tap'
    SWIPE_DOWN = 'swipe_down'
    SWIPE_UP = 'swipe_up'
    SWIPE_LEFT = 'swipe_left'
    SWIPE_RIGHT = 'swipe_right'
    PRESS_KEY_CODE = 'press_key_code'
    #取值和赋值
    SET_VALUE = 'set_value'
    GET_VALUE = 'get_value'
    GET_CONTENT_DESC = "get_content_desc"

    #其他参数
    WAIT_TIME = 20
    RE_CONNECT = 1  # 是否打开失败后再次运行一次用例
