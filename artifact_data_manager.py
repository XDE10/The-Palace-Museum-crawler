import re, traceback
from errors import *
from artifact_types import *
import logging
from errors import *

logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', encoding='utf-8')

def extract_table_info(row, artifact_type, info_text, artifact_total_num, artifact_num, page, line_num):
    # 创建文物对象
    columns = row.find_all('td')
    if artifact_type in class_mapping:
        artifact = class_mapping[artifact_type]()
        
        # 设置对象属性
        artifact.update_info("文物名称", columns[0].text.strip())
        artifact.update_info("时代", columns[1].text.strip() or "未知")
        artifact.update_info("文物简介", info_text)
    else:
        print('该文物类型不存在')

    # 获取图片链接
    try:
        img_link = row.find("img", src=re.compile(r'/Uploads/.*\.(jpg|jpeg|png)|https?://.*\.(jpg|jpeg|png)|/Public.*?\.(jpg|jpeg|png)'))
        #img_link = row.find("img", src=re.compile(r'https?://.*\.(jpg|jpeg|png)|/Public.*?\.(jpg|jpeg|png)'))
        if img_link is None:
            error_message = (
                f'图片链接获取失败——'
                f'{artifact_total_num} - {type_mapping[artifact_type]}-第 {artifact_num} 件文物-'
                f'第 {page} 页第 {line_num} 行'
                '\n\n' + '-'*80 + '\n'
            )
            raise ImageLinkError(error_message)

        if 'http' in img_link or 'https' in img_link:
            image_source = img_link["src"]
        else:
            image_source = 'http://www.dpm.org.cn' + img_link["src"]

    except ImageLinkError as e:
        # 在发生异常时的处理逻辑
        logging.error(f"以下文物在处理图片链接时发生异常", exc_info=True)
        print(f"以下文物在处理图片链接时发生异常:")
        image_source = '图片链接异常'

    artifact.update_info("图片链接", image_source)

    if artifact_type == "ceramics":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("窑口", columns[3].text.strip() or "未知")

    elif artifact_type == "paints":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("作者", columns[3].text.strip() or "未知")

    elif artifact_type == "handwritings":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("作者", columns[3].text.strip() or "未知")

    elif artifact_type == "impress":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "bronzes":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "enamels":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "lacquerwares":
        artifact.update_info("工艺", columns[2].text.strip() or "未知")

    elif artifact_type == "sculptures":
        artifact.update_info("材质", columns[2].text.strip() or "未知")

    elif artifact_type == "tinwares":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "jades":
        artifact.update_info("文化类型", columns[2].text.strip() or "未知")

    elif artifact_type == "seals":
        artifact.update_info("作者", columns[2].text.strip() or "未知")

    elif artifact_type == "embroiders":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("种类", columns[3].text.strip() or "未知")

    elif artifact_type == "studies":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "clocks":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("产地", columns[3].text.strip() or "未知")

    elif artifact_type == "glasses":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "bamboos":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("制作者", columns[3].text.strip() or "未知")

    elif artifact_type == "religions":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "musics":
        artifact.update_info("分类", columns[2].text.strip() or "未知")

    elif artifact_type == "utensils":
        artifact.update_info("分类", columns[2].text.strip() or "未知")
        artifact.update_info("产地", columns[3].text.strip() or "未知")

    elif artifact_type == "foreigns":
        artifact.update_info("产地", columns[2].text.strip() or "未知")

    elif artifact_type == "buildings":
        artifact.update_info("建筑形式", columns[2].text.strip() or "未知")
        artifact.update_info("区域", columns[3].text.strip() or "未知")

    elif artifact_type == "ancients":
        artifact.update_info("版本", columns[2].text.strip() or "未知")

    return artifact