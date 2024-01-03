import re, time, logging, traceback, sys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from artifact_types import *
from artifact_data_manager import *
from errors import *
import csv_writer, excel_append
import logging

logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', encoding='utf-8')

error_messages = []  # 在全局变量中记录错误信息
global_driver = None  # 全局变量 driver
current_artifact_type = None  # 存储文物类型
artifact_total_num = 0  # 存储总文物的数量
artifact_num = 0  # 存储单个文物类型的数量
ancient_text = None  # 存储古籍分类
ancient_num = 0  # 存储古籍各分类数量

def process_table(parent_div):
    if parent_div:
        tables = parent_div.find_all('div', class_='table1')
        for table in tables:
            tbody = table.find('tbody')
            if tbody:
                # 通过设置flag来跳过表头
                first_row = True
                page = extract_page_number()
                line_num = 0
                for row in tbody.find_all('tr'):
                    if first_row:  # 如果是第一行，跳过
                        first_row = False
                        continue
                    line_num += 1
                    process_artifact_row(row, page, line_num)
            else:
                print("错误: 无法找到<tbody>标签")
    else:
        print("错误: 无法找到包含文物信息的父级<div>")


def process_artifact_row(row, page, line_num):
    link = row.find("a", href=re.compile(r'/(collection|explore|ancient)/.+?/\d+'))
    href = link["href"]
    intro_url = "http://www.dpm.org.cn" + href

    # 记录当前窗口句柄
    current_window_handle = global_driver.current_window_handle

    # 打开新标签页
    open_new_tab()
    global_driver.get(intro_url)

    # 等待页面加载完成
    time.sleep(5)

    # 进一步提取信息，创建文物对象等
    process_artifact_details(row, page, line_num)

    # 关闭当前标签页
    global_driver.close()

    # 切换回到原来的窗口句柄
    global_driver.switch_to.window(current_window_handle)


def process_artifact_details(row, page, line_num):
    global ancient_text
    global artifact_total_num
    global artifact_num
    global ancient_num

    artifact_html = global_driver.page_source
    artifact_soup = BeautifulSoup(artifact_html, "html.parser") 

    artifact_total_num += 1
    artifact_num += 1
    ancient_num += 1

    # 获取文物简介并创建文物对象
    content_edit_div = artifact_soup.find('div', class_='content_edit')
    if content_edit_div:
        info_tags = content_edit_div.find_all('p')
        # info_text = extract_artifacts_info(info_tags)
        info_text = None

        try:
            if not info_text:
                error_message = (
                    f'文物简介未找到——'
                    f'{artifact_total_num} - {type_mapping[current_artifact_type]}'
                    f'-{ancient_text + "-" if current_artifact_type == Ancients else ""}第 {artifact_num} 件文物-'
                    f'第 {page} 页第 {line_num} 行'
                    '\n\n' + '-'*80 + '\n'
                )  
                raise ArtifactIntroError(error_message)
        except ArtifactIntroError as e:
            # 在发生异常时的处理逻辑
            logging.error(f"以下文物在获取文物简介时发生异常", exc_info=True)
            print(f"以下文物在获取文物简介时发生异常:")
            info_text  = '文物简介异常'
        

        artifact = extract_table_info(row, current_artifact_type, info_text, artifact_total_num, artifact_num, page, line_num)

        # 把值导入古籍的分类属性 
        if ancient_text:
            artifact.update_info("分类", ancient_text)

        # excel_append.main(artifact_instances)
        # csv_writer.create_csv_files('output_csv', artifact_instances)

        if current_artifact_type != 'ancients':
            print(f'{artifact_total_num} - {type_mapping[current_artifact_type]}-第 {artifact_num} 件文物完成-' + artifact.info['文物名称'])
        else:
            print(f'{artifact_total_num} - {type_mapping[current_artifact_type]}-{ancient_text}-第 {artifact_num} 件文物完成-' + artifact.info['文物名称'])

    else:
        print("错误: 无法找到包含文物信息的<div>标签")


def extract_artifacts_info(info_tags):
    # 处理每个 <p> 标签
    for info_tag in info_tags:
        # 删除不需要的部分
        for span in info_tag.find_all("span", class_="lemma-item", style="display:none;"):
            span.decompose()

    # 连接所有非空 <p> 标签的文本内容
    info_text = ' '.join(p_tag.get_text(strip=True) for p_tag in info_tags if p_tag.get_text(strip=True))

    # 将英文逗号替换为中文逗号，删除所有空格
    info_text = info_text.replace(',', '，').replace(' ', '').replace('　', '').replace('\xa0', '')

    return info_text


def open_new_tab():
    global_driver.execute_script("window.open();")
    new_tab_handle = new_tab_handle = global_driver.window_handles[-1]
    global_driver.switch_to.window(new_tab_handle)


# 设置全局 driver 的函数
def set_global_driver(driver):
    global global_driver
    global_driver = driver


def extract_page_number():
    html_content = global_driver.page_source
    soup = BeautifulSoup(html_content, "html.parser") 
    
    # 使用BeautifulSoup解析HTML  
    soup = BeautifulSoup(html_content, 'html.parser')  
    
    # 找到包含页数的<a>标签  
    current_page_link = soup.find('a', class_='now')  
    
    # 提取页数  
    page_number = current_page_link.text
    return page_number 


def click_next_page():
    try:
        # 等待下一页按钮出现并可点击
        wait = WebDriverWait(global_driver, 10)
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='next']")))
        next_page_button.click()
        
        # 等待新页面加载完成
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table1')))
        time.sleep(5)  # 等待一段时间，确保页面完全加载

    except Exception as e:
        raise e  # 无法点击下一页按钮，直接返回

   
def jump_to_page(page):
    # 找到搜索框元素
    search_box = global_driver.find_element(By.ID, "text_se")

    # 在搜索框中输入查询内容
    search_box.clear()
    search_box.send_keys(page)

    # 找到跳转按钮元素
    jump_button = global_driver.find_element(By.ID, "btn_new")

    # 点击跳转按钮
    jump_button.click()

    # 等待页面加载
    time.sleep(5)


def process_ancient_link(link):
    global ancient_text

    ancient_text = text_content_list[link_elements.index(link)]

    # 打开新的标签页
    open_new_tab()

    # 进一步处理链接
    global_driver.get(link)

    # 等待页面加载完成
    time.sleep(5)

    while True:
        list_html = global_driver.page_source
        list_soup = BeautifulSoup(list_html, "html.parser")
        parent_div = list_soup.find('div', class_='wrap parentsHtml')
        page = extract_page_number()
        print('*'*50 + f'第 25 个文物类型——古籍-{ancient_text}-第 {page} 页' + '*'*50)
        process_table(parent_div)
        print('*'*50 + f'第 25 个文物类型——古籍-{ancient_text}-第 {page} 页已完成' + '*'*50 + '\n')
        try:
            # 点击下一页按钮
            click_next_page()
        except Exception as e:
            break


def main(url, artifact_type_number):
    global ancient_text
    global current_artifact_type
    global artifact_num
    global ancient_num
    global error_messages

    error_messages = []

    # 获取默认的日志记录器  
    logger = logging.getLogger()  
    
    # 设置日志级别  
    logger.setLevel(logging.ERROR)  
    
    # 屏蔽特定的日志信息  
    logger.getChild('CONSOLE').setLevel(logging.ERROR)   
    
    match_artifact = re.search(r'/collection/(.+?)\.html|/explore/(.+?)\.html', url)
    current_artifact_type = match_artifact.group(1) or match_artifact.group(2)

    # 获取当前窗口句柄
    current_window_handle = global_driver.current_window_handle

    # 打开新的标签页
    open_new_tab()

    # 在新标签页中打开链接
    global_driver.get(url)
    
    # 等待页面加载    
    time.sleep(5) 

    if current_artifact_type != 'ancients':
        while True:
            html = global_driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            print('*'*50 + f'第 {artifact_type_number} 个文物类型——{type_mapping[current_artifact_type]}-第 {page} 页')
            parent_div = soup.find('div', class_='wrap parentsHtml')
            process_table(parent_div)

            page = extract_page_number()
            print('*'*50 + f'第 {artifact_type_number} 个文物类型——{type_mapping[current_artifact_type]}-第 {page} 页已完成' + '*'*50 + '\n')
            break

            try:
                click_next_page()
            except Exception as e:
                print(f'第 {artifact_type_number} 个文物类型——{type_mapping[current_artifact_type]}已全部完成——总数 {artifact_num}')
                break
    else:
        # 查找 'text' div 元素
        text_div = global_driver.find_element(By.CLASS_NAME, 'text')

        # 提取链接文本内容并放入列表
        global text_content_list, link_elements
        links = text_div.find_elements(By.TAG_NAME, 'a')
        text_content_list = [link.text for link in links]
    
        link_elements = [link.get_attribute('href') for link in text_div.find_elements(By.TAG_NAME, 'a')]  

        ancient_page = 0
        for link in link_elements:
            process_ancient_link(link)
            print(f'古籍-第 {ancient_page+1} 个分类-{text_content_list[ancient_page]}-已完成——总数 {ancient_num}' + '\n')
            ancient_num = 0
            ancient_page += 1
        print(f'第 {artifact_type_number} 个文物类型——{type_mapping[current_artifact_type]}已全部完成——总数 {artifact_num}' + '\n')

    artifact_num = 0


if __name__ == "__main__":
    main()


