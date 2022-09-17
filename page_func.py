from lib2to3.pgen2 import driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime
import warnings
import random
warnings.filterwarnings('ignore')


def login(driver, user_name, password, retry=0):
    if retry == 3:
        return '门户登录失败\n'

    print('门户登录中...')

    
    driver.get('https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https%3A%2F%2Fportal.pku.edu.cn%2Fportal2017%2FssoLogin.do')

    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'logon_button')))

    driver.find_element(By.ID,"user_name").send_keys("2000012511")
    
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    
    driver.find_element(By.ID,"password").send_keys("ning20020510")
    
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    driver.find_element(By.ID,'logon_button').click()
    time.sleep(1)
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, 'all')))
        print('门户登录成功')
        return '门户登录成功\n'
    except:
        print('Retrying...')
        login(driver, user_name, password, retry + 1)


def go_to_venue(driver, venue, retry=0):
    if retry == 3:
        print("进入预约 %s 界面失败" % venue)
        log_str = "进入预约 %s 界面失败\n" % venue
        return False, log_str

    print("进入预约 %s 界面" % venue)
    log_str = "进入预约 %s 界面\n" % venue

    try:
        butt_all = driver.find_element(By.ID,'all')
        driver.execute_script('arguments[0].click();', butt_all)
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'venues')))

        driver.find_element(By.ID,'venues').click()

        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 10).until_not(
                EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
        WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div[1]/div[2]")))
        driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div/div[3]/div/div[1]/div/div[2]/div[2]").click()
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div [contains(text(),\'%s\')]' % venue)))
        
        driver.find_element(By.XPATH,
            '//div [contains(text(),\'%s\')]' % venue).click()
        status = True
        log_str += "进入预约 %s 界面成功\n" % venue
    except:
        print("retrying")
        status, log_str = go_to_venue(driver, venue, retry + 1)
    return status, log_str


def click_agree(driver):
    print("点击同意")
    log_str = "点击同意\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'ivu-checkbox-wrapper')))
    time.sleep(0.1)
    driver.find_element(By.CLASS_NAME,'ivu-checkbox-wrapper').click()
    print("点击同意成功\n")
    log_str += "点击同意成功\n"
    return log_str


def judge_exceeds_days_limit(start_time, end_time):
    start_time_list = start_time.split('/')
    end_time_list = end_time.split('/')
    print(start_time_list, end_time_list)
    now = datetime.datetime.today()
    today = datetime.datetime.strptime(str(now)[:10], "%Y-%m-%d")
    time_hour = datetime.datetime.strptime(
        str(now).split()[1][:-7], "%H:%M:%S")
    time_11_55 = datetime.datetime.strptime(
        "11:55:00", "%H:%M:%S")
    # time_11_55 = datetime.datetime.strptime(
    #     str(now).split()[1][:-7], "%H:%M:%S")

    start_time_list_new = []
    end_time_list_new = []
    delta_day_list = []

    for k in range(len(start_time_list)):
        start_time = start_time_list[k]
        end_time = end_time_list[k]
        if len(start_time) > 8:
            date = datetime.datetime.strptime(
                start_time.split('-')[0], "%Y%m%d")
            delta_day = (date-today).days
        else:
            delta_day = (int(start_time[0])+6-today.weekday()) % 7
            date = today+datetime.timedelta(days=delta_day)
        print("日期:", str(date).split()[0])
        # print(delta_day)
        if delta_day > 3 or (delta_day == 3 and (time_hour < time_11_55)):
            print("只能在当天中午11:55后预约未来3天以内的场馆")
            log_str = "只能在当天中午11:55后预约未来3天以内的场馆\n"
            break
        else:
            start_time_list_new.append(start_time)
            end_time_list_new.append(end_time)
            delta_day_list.append(delta_day)
            print("在预约可预约日期范围内")
            log_str = "在预约可预约日期范围内\n"
    return start_time_list_new, end_time_list_new, delta_day_list, log_str


def book(driver, start_time_list, end_time_list, delta_day_list, venue_num=-1):
    print("查找空闲场地")
    log_str = "查找空闲场地\n"

    def judge_close_to_time_12():
        now = datetime.datetime.today()
        time_hour = datetime.datetime.strptime(
            str(now).split()[1][:-7], "%H:%M:%S")
        time_11_55 = datetime.datetime.strptime(
            "11:55:00", "%H:%M:%S")
        time_12 = datetime.datetime.strptime(
            "12:00:00", "%H:%M:%S")
        # time_11_55 = datetime.datetime.strptime(
        #     str(now).split()[1][:-7], "%H:%M:%S")
        # time_12 = time_11_55+datetime.timedelta(minutes=1)
        if time_hour < time_11_55:
            return 0
        elif time_11_55 < time_hour < time_12:
            return 1
        elif time_hour > time_12:
            return 2

    def judge_in_time_range(start_time, end_time, venue_time_range):
        vt = venue_time_range.split('-')
        vt_start_time = datetime.datetime.strptime(vt[0], "%H:%M")
        vt_end_time = datetime.datetime.strptime(vt[1], "%H:%M")
        if start_time <= vt_start_time and vt_end_time <= end_time:
            return True
        else:
            return False

    def move_to_date(delta_day):
        for i in range(delta_day):
            WebDriverWait(driver, 10).until_not(
                EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
            driver.find_element(By.XPATH,
                '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div/button[2]/i').click()
            time.sleep(0.2)

    def click_free(start_time, end_time, venue_num, table_num):
        trs = driver.find_elements(By.TAG_NAME,'tr')
        # 防止表格没加载出来
        no_table_flag = 0
        while trs[1].find_elements(By.TAG_NAME,
                'td')[0].find_element(By.TAG_NAME,'div').text == "时间段":
            no_table_flag += 1
            time.sleep(0.2)
            trs = driver.find_elements(By.TAG_NAME,'tr')
            if no_table_flag > 10:
                driver.refresh()
                no_table_flag = 0
                move_to_date(delta_day)
        trs_list = []
        for i in range(1, len(trs)-2):
            vt = trs[i].find_elements(By.TAG_NAME,
                'td')[0].find_element(By.TAG_NAME,'div').text
            if judge_in_time_range(start_time, end_time, vt):
                trs_list.append(trs[i].find_elements(By.TAG_NAME,
                    'td'))
        if len(trs_list) == 0:
            return False, -1, 0

        j_list = [x for x in range(1, len(trs_list[0]))]
        print(venue_num, table_num, j_list)
        if venue_num != -1 and (venue_num-table_num in j_list):
            flag = False
            for i in range(len(trs_list)):
                class_name = trs_list[i][venue_num-table_num].find_element(By.TAG_NAME,
                    'div').get_attribute("class")
                print(class_name)
                if class_name.split()[2] == 'free':
                    flag = True
                    break
        elif venue_num != -1 and (venue_num-table_num not in j_list):
            return False, venue_num, table_num + len(j_list)
        else:
            # 随机点一列free的，防止每次都点第一列
            random.shuffle(j_list)
            print(j_list)
            for j in j_list:
                flag = False
                for i in range(len(trs_list)):
                    class_name = trs_list[i][j].find_element(By.TAG_NAME,
                        'div').get_attribute("class")
                    print(class_name)
                    if class_name.split()[2] == 'free':
                        flag = True
                        venue_num = j+table_num
                        break
        if flag:
            for i in range(len(trs_list)):
                WebDriverWait(driver, 10).until_not(
                    EC.visibility_of_element_located((By.CLASS_NAME,
                                                      "loading.ivu-spin.ivu-spin-large.ivu-spin-fix.fade-leave-active.fade-leave-to")))
                trs_list[i][venue_num-table_num].find_element(By.TAG_NAME,
                    'div').click()
            return True, venue_num, table_num + len(j_list)
        return False, venue_num, table_num + len(j_list)

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div/div/div[1]/div/div/input')))
    # 若接近但是没到12点，停留在此页面
    flag = judge_close_to_time_12()
    if flag == 1:
        while True:
            flag = judge_close_to_time_12()
            if flag == 2:
                break
            else:
                time.sleep(0.5)
        driver.refresh()
        WebDriverWait(driver, 5).until_not(
            EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))

    for k in range(len(start_time_list)):
        start_time = start_time_list[k]
        end_time = end_time_list[k]
        delta_day = delta_day_list[k]

        if k != 0:
            driver.refresh()
            time.sleep(0.5)

        move_to_date(delta_day)

        start_time = datetime.datetime.strptime(
            start_time.split('-')[1], "%H%M")
        end_time = datetime.datetime.strptime(end_time.split('-')[1], "%H%M")
        print("开始时间:%s" % str(start_time).split()[1])
        print("结束时间:%s" % str(end_time).split()[1])

        status, venue_num, table_num = click_free(
            start_time, end_time, venue_num, 0)
        # 如果第一页没有，就往后翻，直到不存在下一页
        while not status:
            next_table = driver.find_elements(By.XPATH,
                '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i')
            WebDriverWait(driver, 10).until_not(
                EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
            time.sleep(0.1)
            if len(next_table) > 0:
                driver.find_element(By.XPATH,
                    '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i').click()
                status, venue_num, table_num = click_free(
                    start_time, end_time, venue_num, table_num)
            else:
                break
        if status:
            log_str += "找到空闲场地，场地编号为%d\n" % venue_num
            print("找到空闲场地，场地编号为%d\n" % venue_num)
            now = datetime.datetime.now()
            today = datetime.datetime.strptime(str(now)[:10], "%Y-%m-%d")
            date = today+datetime.timedelta(days=delta_day)
            return status, log_str, str(date)[:10]+str(start_time)[10:], str(date)[:10]+str(end_time)[10:], venue_num
        else:
            log_str += "没有空余场地\n"
            print("没有空余场地\n")
    return status, log_str, None, None, None


def click_book(driver):
    print("确定预约")
    log_str = "确定预约\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]')))
    driver.find_element(By.XPATH,
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]').click()
    time.sleep(1)
    print("确定预约成功")
    log_str += "确定预约成功\n"
    return log_str


def click_submit_order(driver):
    print("提交订单")
    log_str = "提交订单\n"
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading.ivu-spin.ivu-spin-large.ivu-spin-fix")))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'payHandleItem')))
    driver.find_element(By.XPATH,
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]').click()
    time.sleep(1)
    #result = EC.alert_is_present()(driver)
    print("提交订单成功")
    log_str += "提交订单成功\n"
    return log_str

def mouse_move(driver,x):

    print("滑动滑块")
    log_book = "滑动滑块\n"

    # 定位鼠标
    mouse = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div')
    # ------------鼠标滑动操作------------
    from selenium.webdriver.common.action_chains import ActionChains
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(mouse, x, 0)
    # 执行动作
    action.perform()

    print("滑动滑块成功")
    log_book = "滑动滑块成功\n"

def click_pay(driver):
    print("付款（校园卡）")
    log_str = "付款（校园卡）\n"
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(2)
    driver.find_element(By.XPATH,
        '/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div[8]/div[2]/button').click()
    print("付款成功")
    log_str += "付款成功\n"
    return log_str


if __name__ == '__main__':
    pass
