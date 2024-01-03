import pandas as pd
from artifact_types import class_mapping

def create_excel_file(file_path, artifact_instances):
    # 创建 ExcelWriter 对象
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # 循环处理每个类
    for class_name, class_type in class_mapping.items():
        # 获取类的属性，包括 artifact_type
        attributes = ["artifact_type"] + list(class_type().info.keys())

        # 创建一个DataFrame用于存储对象的属性，指定数据类型
        df = pd.DataFrame(columns=attributes, dtype='object')

        # 将每个对象的属性值添加到DataFrame
        for instance in artifact_instances:
            if isinstance(instance, class_type):
                # 添加 artifact_type 属性值
                instance_info = {"artifact_type": instance.artifact_type}
                instance_info.update(instance.info)
                df = pd.concat([df, pd.DataFrame([instance_info], dtype='object')], ignore_index=True)

        # 检查 DataFrame 是否为空
        if not df.empty:
            # 将DataFrame写入Excel文件，每个类对应一个表单
            df.to_excel(writer, sheet_name=class_name, index=False)

            # 获取底层的 xlsxwriter.Workbook 对象
            workbook = writer.book

            # 获取当前工作表的 xlsxwriter.Worksheet 对象
            worksheet = writer.sheets[class_name]

            # 调整单元格的宽度以适应内容
            for i, col in enumerate(df.columns):
                max_len = df[col].astype(str).apply(len).max()
                worksheet.set_column(i, i, max_len + 2)  # 2 是为了留有一些额外空间
                worksheet.set_column(i, i, None, None, {'text_wrap': True})

    # 关闭writer前检查是否有至少一个表单被写入
    if writer.sheets:
        writer.close()
    else:
        print("没有数据被写入 Excel 文件。") 

