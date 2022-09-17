# -*- coding: utf-8 -*-
import cv2
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

# 抓取验证码图片的URL


def get_img(driver):

    print("获取图片")
    log_book = "获取图片\n"

    bg_xpath = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/img')
    
    # 获取图片位置和宽高
    bg_location = bg_xpath.location
    bg_size = bg_xpath.size
    
    # 返回左上角和右下角的坐标
    bg_top,bg_bottom,bg_left,bg_right = bg_location['y'], bg_location['y']+bg_size['height'], bg_location['x'], bg_location['x']+bg_size['width']


    tp_xpath = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/img')
    tp_location = tp_xpath.location
    tp_size = tp_xpath.size
    tp_top,tp_bottom,tp_left,tp_right = tp_location['y'], tp_location['y']+tp_size['height'], tp_location['x'], tp_location['x']+tp_size['width']

    # 截取整张网页图片
    screenshot_orgin = driver.get_screenshot_as_png()
    screenshot_bg = Image.open(BytesIO(screenshot_orgin))
    screenshot_tp = Image.open(BytesIO(screenshot_orgin))

    # 将网页中需要的图片通过坐标裁剪出来
    bg_screenshot = screenshot_bg.crop((bg_left + 50, bg_top, bg_right, bg_bottom))
    tp_screenshot = screenshot_tp.crop((tp_left, tp_top, tp_right, tp_bottom))

    bg_screenshot.save(r'C:\Users\Thor\Desktop\PKUAutoBookingVenues\pngs\bg.png')
    tp_screenshot.save(r'C:\Users\Thor\Desktop\PKUAutoBookingVenues\pngs\tp.png')

    print("获取图片成功")
    log_book = "获取图片成功\n"

    print("bp_size:",bg_size['width'])
    
    return log_book




# 获得鼠标移动距离

def get_move_distance():

    print("计算鼠标移动距离")
    log_book = "计算鼠标距离\n"

    bg_img = cv2.imread(r'C:\Users\Thor\Desktop\PKUAutoBookingVenues\pngs\bg.png',0)
    tp_img = cv2.imread(r'C:\Users\Thor\Desktop\PKUAutoBookingVenues\pngs\tp.png',0)

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 500)
    tp_edge = cv2.Canny(tp_img, 100, 500)

    
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)

    locations = cv2.minMaxLoc(res)  # 寻找最优匹配

    X = locations[3][0] + 50

    print("计算鼠标移动距离成功")
    log_book = "计算鼠标移动距离成功\n"
    
    return X,log_book
