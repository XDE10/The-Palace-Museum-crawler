import csv
from artifact_types import class_mapping

def create_csv_files(output_folder, artifact_instances):
    for class_name, class_type in class_mapping.items():
        # 获取类的属性
        attributes = list(class_type().info.keys())

        # 创建CSV文件
        file_path = f"{output_folder}/{class_name}.csv"
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)

                # 写入每个对象的属性值
                for instance in artifact_instances:
                    if isinstance(instance, class_type):
                        row_data = [instance.info.get(attr, "") for attr in attributes]
                        csv_writer.writerow(row_data)
                        print(f"Writing to {file_path}: {row_data}")
        except Exception as e:
            print(f"An error occurred while creating {file_path}: {e}")
