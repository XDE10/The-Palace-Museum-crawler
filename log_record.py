def log_processed_artifact(art_num, art_type, art_page, art_row):
    with open('processed_artifacts.txt', 'a') as file:
        file.write(f'{art_num} - {art_type} - 第 {art_page} 页第 {art_row} 行' + '\n')





