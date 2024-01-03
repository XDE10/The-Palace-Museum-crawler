import logging

logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', encoding='utf-8')

class ImageLinkError(Exception):
    """图片链接获取失败异常。"""
    pass

class ArtifactIntroError(Exception):
    """文物简介获取失败异常。"""
    pass

class PageLoadTimeoutError(Exception):
    """网页加载超时异常。"""
    pass

class ProcessTableError(Exception):
    """处理文物表格异常。"""
    pass

class ProcessArtifactRowError(Exception):
    """处理文物行异常。"""
    pass

class ProcessArtifactDetailsError(Exception):
    """处理文物详情异常。"""
    pass