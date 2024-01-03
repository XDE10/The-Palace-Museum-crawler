class Artifact:
    def __init__(self, artifact_type):
        self.artifact_type = artifact_type
        self.info = {"文物名称": "", "时代": "", "图片链接": ""}
        
    def update_info(self, name, value):
        self.info[name] = value

    # 用于调试
    def print_info(self):
        print(f"文物类型: {self.artifact_type}")
        for key, value in self.info.items():
            print(f"{key}: {value}")


class Ceramics(Artifact):
    def __init__(self):
        super().__init__("陶瓷")
        self.info["分类"] = ""
        self.info["窑口"] = ""
        self.info["文物简介"] = ""


class Paints(Artifact):
    def __init__(self):
        super().__init__("绘画")
        self.info["分类"] = ""
        self.info["作者"] = ""
        self.info["文物简介"] = ""


class Handwritings(Artifact):
    def __init__(self):
        super().__init__("法书")
        self.info["分类"] = ""
        self.info["作者"] = ""
        self.info["文物简介"] = ""


class Impress(Artifact):
    def __init__(self):
        super().__init__("铭刻")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Bronzes(Artifact):
    def __init__(self):
        super().__init__("青铜器")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Enamels(Artifact):
    def __init__(self):
        super().__init__("珐琅")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Lacquerwares(Artifact):
    def __init__(self):
        super().__init__("漆器")
        self.info["工艺"] = ""
        self.info["文物简介"] = ""


class Sculptures(Artifact):
    def __init__(self):
        super().__init__("雕塑")
        self.info["材质"] = ""
        self.info["文物简介"] = ""


class Tinwares(Artifact):
    def __init__(self):
        super().__init__("金银锡器")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Jades(Artifact):
    def __init__(self):
        super().__init__("玉石器")
        self.info["文化类型"] = ""
        self.info["文物简介"] = ""


class Seals(Artifact):
    def __init__(self):
        super().__init__("玺印")
        self.info["作者"] = ""
        self.info["文物简介"] = ""


class Embroiders(Artifact):
    def __init__(self):
        super().__init__("织绣")
        self.info["分类"] = ""
        self.info["种类"] = ""
        self.info["文物简介"] = ""


class Studies(Artifact):
    def __init__(self):
        super().__init__("文房用品")
        self.info["分类"] = ""    
        self.info["文物简介"] = ""    


class Gears(Artifact):
    def __init__(self):
        super().__init__("家具")
        self.info["文物简介"] = ""


class Clocks(Artifact):
    def __init__(self):
        super().__init__("钟表仪器")
        self.info["分类"] = ""
        self.info["产地"] = ""
        self.info["文物简介"] = ""


class Glasses(Artifact):
    def __init__(self):
        super().__init__("玻璃器")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Bamboos(Artifact):
    def __init__(self):
        super().__init__("竹木角牙匏")
        self.info["分类"] = ""
        self.info["制作者"] = ""
        self.info["文物简介"] = ""


class Religions(Artifact):
    def __init__(self):
        super().__init__("宫廷宗教")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Jewelrys(Artifact):
    def __init__(self):
        super().__init__("首饰")
        self.info["文物简介"] = ""


class Defenses(Artifact):
    def __init__(self):
        super().__init__("武备依仗")
        self.info["文物简介"] = ""


class Musics(Artifact):
    def __init__(self):
        super().__init__("音乐戏曲")
        self.info["分类"] = ""
        self.info["文物简介"] = ""


class Utensils(Artifact):
    def __init__(self):
        super().__init__("生活器具")
        self.info["分类"] = ""
        self.info["产地"] = ""
        self.info["文物简介"] = ""


class Foreigns(Artifact):
    def __init__(self):
        super().__init__("外国文物")
        self.info["产地"] = ""
        self.info["文物简介"] = ""

    
class Buildings(Artifact):
    def __init__(self):
        super().__init__("建筑")
        self.info["建筑形式"] = ""
        self.info["区域"] = ""
        self.info["文物简介"] = ""


class Ancients(Artifact):
    def __init__(self):
        super().__init__("古籍")
        self.info["分类"] = ""
        self.info["版本"] = ""
        self.info["文物简介"] = ""


class_mapping = {
    "ceramics": Ceramics,
    "paints": Paints,
    "handwritings": Handwritings,
    "impress": Impress,
    "bronzes": Bronzes,
    "enamels": Enamels,
    "lacquerwares": Lacquerwares,
    "sculptures": Sculptures,
    "tinwares": Tinwares,
    "jades": Jades,
    "seals": Seals,
    "embroiders": Embroiders,
    "studies": Studies,
    "gears": Gears,
    "clocks": Clocks,
    "glasses": Glasses,
    "bamboos": Bamboos,
    "religions": Religions,
    "jewelrys": Jewelrys,
    "defenses": Defenses,
    "musics": Musics,
    "utensils": Utensils,
    "foreigns": Foreigns,
    "buildings": Buildings,
    "ancients": Ancients,
}

type_mapping = {
    "ceramics": "陶瓷",
    "paints": "绘画",
    "handwritings": "法书",
    "impress": "铭刻",
    "bronzes": "青铜器",
    "enamels": "珐琅",
    "lacquerwares": "漆器",
    "sculptures": "雕塑",
    "tinwares": "金银锡器",
    "jades": "玉石器",
    "seals": "玺印",
    "embroiders": "织绣",
    "studies": "文房用品",
    "gears": "家具",
    "clocks": "钟表仪器",
    "glasses": "玻璃器",
    "bamboos": "竹木牙角匏",
    "religions": "宫廷宗教",
    "jewelrys": "首饰",
    "defenses": "武备仪仗",
    "musics": "音乐戏曲",
    "utensils": "生活器具",
    "foreigns": "外国文物",
    "buildings": "建筑",
    "ancients": "古籍",
}