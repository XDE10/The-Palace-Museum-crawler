import openpyxl
def main(artifact_instances):
    # 指定文件路径
    file_full_path = '玻璃器.xlsx'
    # sheet名称
    sheet_name = '玻璃器'
 
    # 获取指定的文件
    wb = openpyxl.load_workbook(file_full_path)
    # 获取指定的sheet
    ws = wb[sheet_name]
    # 获得最大行数
    max_row_num = ws.max_row

    # 将当前行设置为最大行数
    ws._current_row = max_row_num
 
    # 使用append方法，将行数据按行追加写入
    for artifact in artifact_instances:
        ws.append(['玻璃器'] + list(artifact.info.values()))
 
    # 保存文件
    wb.save('玻璃器.xlsx')

if __name__ == '__main__':
    main()