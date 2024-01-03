from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from artifact_types import *
import time, artifact_details_crawler
import excel_writer, csv_writer

# 创建ChromeOptions对象并启用无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')  # 禁用除了错误信息之外的所有日志输出

# 创建WebDriver并指定ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# 设置全局变量 driver
artifact_details_crawler.set_global_driver(driver)

# 打开故宫博物院藏品网页
url = 'https://www.dpm.org.cn/explore/collections.html'
driver.get(url)

# 等待一段时间，确保页面加载完成
time.sleep(3)

unwanted_urls = [  
    'https://www.dpm.org.cn/shuziduobaoge.html',  
    'https://www.dpm.org.cn/explores/courts.html',  
    'https://www.dpm.org.cn/explore/protects.html',  
    'https://www.dpm.org.cn/explore/cultures.html'  
]  

# 找到所有包含指定连接的元素
box_elements = driver.find_elements(By.CLASS_NAME, 'box')

# 找到所有包含 <a> 标签的 <div> 元素
div_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "box")]//div[contains(@class, "div")]/a')
  

href_list = [div_element.get_attribute("href") for div_element in div_elements if div_element.get_attribute("href") not in unwanted_urls]  

# 逐个点击链接，用新标签页打开
type_num = 0
for link in href_list:
    # 获取当前窗口句柄
    current_window_handle = driver.current_window_handle

    type_num += 1

    if link != 'https://www.dpm.org.cn/explore/ancients.html':
        continue

    artifact_type = link.split('/')[-1].split('.')[0]

    print('*'*50 + f'第 {type_num} 个文物类型——{type_mapping[artifact_type]}' + '*'*50)
    # 进一步提取信息
    artifact_details_crawler.main(link, type_num)

    driver.close()
    driver.switch_to.window(current_window_handle)

print('非常成功！！！')
print('文物已全部处理完成')

# 关闭浏览器
driver.quit()