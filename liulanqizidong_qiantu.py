import csv
import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By



option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=option)

script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
driver.execute_script(script)

try:
    driver.get("https://we.51job.com/api/job/search-pc?api_key=51job&timestamp=&keyword=&searchType=2&function=&industry=01&jobArea=030800&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum=1&requestId=&pageSize=10000&source=1&accountId=225650817&pageCode=sou|sou|soulb")
    time.sleep(2)  # 防止加载缓慢，休眠2秒

    ele_button = driver.find_element(by=By.XPATH, value="//span[@id='nc_1_n1z']")
    ActionChains(driver).click_and_hold(ele_button).perform()
    ActionChains(driver).move_by_offset(255, yoffset=0).perform()
    time.sleep(1)

    ActionChains(driver).release().perform()

    print('结束')
    time.sleep(100)


finally:
    driver.quit()


