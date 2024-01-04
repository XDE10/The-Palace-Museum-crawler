import threading  
  
# 创建线程本地存储对象  
local_data = threading.local()  
  
# 在每个线程中设置变量值  
def set_local_values(driver, artifact_type, artifact_total, artifact_individual, ancient_text, ancient_individual):  
    local_data.driver = driver  
    local_data.current_artifact_type = artifact_type  
    local_data.artifact_total_num = artifact_total  
    local_data.artifact_num = artifact_individual  
    local_data.ancient_text = ancient_text  
    local_data.ancient_num = ancient_individual  
  
# 在每个线程中获取变量值  
def get_local_values():  
    return (local_data.driver, local_data.current_artifact_type, local_data.artifact_total_num, local_data.artifact_num, local_data.ancient_text, local_data.ancient_num)  