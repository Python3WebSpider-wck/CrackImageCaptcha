import time
import re
import tesserocr
from selenium import webdriver
from io import BytesIO
from PIL import Image
from retrying import retry
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np
from selenium.webdriver.common.by import By


THRESHOLD = 100     # 注意：阈值很重要


def preprocess(image):
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > THRESHOLD, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image


@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    browser.get('https://captcha7.scrape.center/')
    # browser.find_element_by_css_selector('.username input[type="text"]').send_keys('admin')
    # browser.find_element_by_css_selector('.password input[type="password"]').send_keys('admin')
    # captcha = browser.find_element_by_css_selector('#captcha')
    browser.find_element(By.CSS_SELECTOR, '.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR, '.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprocess(image)
    # 对验证码进行识别，得到识别结果
    captcha = tesserocr.image_to_text(image)
    print(f"captcha: {captcha}")
    # 识别结果去除一些非字母和数字字符
    captcha = re.sub('[^A-Za-z0-9]', '', captcha)
    # 找到验证码输入框，输入验证码结果
    browser.find_element(By.CSS_SELECTOR, '.captcha input[type="text"]').send_keys(captcha)
    # 点击登录按钮
    browser.find_element(By.CSS_SELECTOR, '.login').click()
    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(., "登录成功")]')))
        time.sleep(3)
        browser.close()
        return True
    except TimeoutException:
        return False


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()
