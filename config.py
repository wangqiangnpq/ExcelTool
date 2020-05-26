from enum import Enum,unique
#Excel目录
Excel_path = "./表格测试"

#表格的字段名的行开始行
key_row = 1
#表格唯一ID的字段开始列
UID_col = 0
#表格数据类型的开始行
type_row = 2
#表格数据的开始行
value_row = 3

#Excel白名单
Start_Write_List = False
Excel_Write_List = [
    "Goods.xlsx"
]

#导出标志
Export_Flag = "IsExport"
@unique
class Excel_Type(Enum):
    int = "int"
    float = "float"
    bool = "bool"
    string = "string"

#生成代码语言类型枚举
@unique
class Export_Type(Enum):
    XML = "XML"
    XML_CPP = "XML_CPP"
    JSON = "JSON"
    JSON_CPP = "JSON_CPP"

#当前生成的语言类型
Current_Export_list = [
    {
        "type":Export_Type.XML.value,
        "checked":False,
        "export_path":"./OutPut/xml/",
        "import_path":"./OutPut/xml"
    },
    {
        "type":Export_Type.XML_CPP.value,
        "checked":True,
        "export_path": "./OutPut/xmlcpp/",
        "import_path": "../resource/excel/"
    },
    {
        "type":Export_Type.JSON.value,
        "checked":False,
        "export_path": "./OutPut/json/",
        "import_path": "./OutPut/json/"
    },
    {
        "type":Export_Type.JSON_CPP.value,
        "checked":True,
        "export_path": "./OutPut/jsoncpp/",
        "import_path": "../resource/excel/"
    },
]

#类型头文件
type_include = {
    Export_Type.XML_CPP.value:
    [
        "#pragma once",
        "#include <string>",
        "#include <iostream>",
        "#include <map>",
        "#include \"../ServerEngine/ServerEngine.h\"",
        "#include \"../ServerEngine/tinyxml/tinyxml2.h\"",
        "using namespace std;",
    ],
    Export_Type.JSON_CPP.value:
    [
        "#pragma once",
        "#include <string>",
        "#include <map>",
        "#include <stdio.h>",
        "#include \"../ServerEngine/ServerEngine.h\"",
        "#include \"../ServerEngine/rapidjson/rapidjson.h\"",
        "#include \"../ServerEngine/rapidjson/document.h\"",
        "using namespace std;",
    ]
}

#类型比对表
type_compair = {
        Export_Type.XML_CPP.value:
        {
            Excel_Type.int.value:"INT32",
            Excel_Type.string.value:"string",
            Excel_Type.bool.value:"BOOL",
            Excel_Type.float.value:"FLOAT"
         },
        Export_Type.JSON_CPP.value:
        {
            Excel_Type.int.value:"INT32",
            Excel_Type.string.value:"string",
            Excel_Type.bool.value:"BOOL",
            Excel_Type.float.value:"FLOAT"
         }
}




