from config import *
def OutFile(path,save_name,save_str):
    import os
    try:
        path = path.strip()
        path = path.rstrip("\\")
        if not os.path.exists(path):
            os.makedirs(path)
            print(path + " 创建成功")
        fd = open(path+save_name, "wt")
        fd.write(save_str)
        fd.close()
    except Exception as e:
        print(path+save_name+" 创建失败 "+str(e))

def Export(filename, key_list, data_type_list, final_value_list, export_type_list):
    if export_type_list["type"] == Export_Type.XML.value :
        ExportXML(filename,key_list,final_value_list,export_type_list)
    elif export_type_list["type"] == Export_Type.XML_CPP.value :
        ExportXMLCPP(filename, key_list, data_type_list, export_type_list)
    elif export_type_list["type"] == Export_Type.JSON.value:
        ExportJSON(filename,key_list,data_type_list,final_value_list,export_type_list)
    elif export_type_list["type"] == Export_Type.JSON_CPP.value :
        ExportJSONCPP(filename, key_list, data_type_list, export_type_list)

def ExportXML(filename,key_list,final_value_list,export_type_list):
    save_str = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    save_str += "<root count="+"\""+str(len(final_value_list))+"\">\n"
    for row in range(0,len(final_value_list)):
        save_str += "   <item "
        for col in range(0,len(final_value_list[row])):
            save_str += str(key_list[col])+"=\""+str(final_value_list[row][col])+"\" "
        save_str += "/>\n"
    save_str += "</root>"
    # 生成文件
    path = export_type_list["export_path"]
    filename = filename+".xml"
    OutFile(path,filename,save_str)

def ExportXMLCPP(filename, key_list, data_type_list, export_type_list):
    save_str = ""
    tran_dict = type_compair[export_type_list["type"]]
    #导出头文件
    inc_list = type_include[export_type_list["type"]]
    for inc_str in inc_list:
        save_str += inc_str+"\n"
    #导出固定命名空间
    save_str += "namespace ExcelXml\n"
    save_str += "{\n"
    #导出结构struct
    save_str += "    struct "+filename+"\n"
    save_str += "    {\n"
    for key_i in range(0,len(key_list)):
        save_str += "        "+tran_dict[data_type_list[key_i]]+" "+key_list[key_i]+";\n"
    save_str += "    };\n"
    #导出解析class
    save_str += "    class " + filename + "Parser\n"
    save_str += "    {\n"
    #--Instance--
    save_str += "    private:\n"
    save_str += "       static "+filename+"Parser* _ins;\n"
    save_str += "    public:\n"
    save_str += "       static "+filename+"Parser& GetInstance()\n"
    save_str += "       {\n"
    save_str += "           if(!_ins)\n"
    save_str += "           {\n"
    save_str += "               _ins = new "+filename + "Parser();\n"
    save_str += "           }\n"
    save_str += "           return *_ins;\n"
    save_str += "       }\n"
    #--map--
    save_str += "   private:\n"
    save_str += "       typedef map<"+tran_dict[data_type_list[UID_col]]+","+filename+"> Map;\n"
    save_str += "       typedef map<" + tran_dict[data_type_list[UID_col]] + "," + filename + ">::iterator Iterator;\n"
    save_str += "       Map _map;\n"
    #--Load--
    save_str += "    public:\n"
    save_str += "       bool Load()\n"
    save_str += "       {\n"
    save_str += "           tinyxml2::XMLDocument doc;\n"
    save_str += "           if (doc.LoadFile(\""+export_type_list["import_path"]+filename+".xml\") != tinyxml2::XMLError::XML_SUCCESS)\n"
    save_str += "           {\n"
    save_str += "               cerr << doc.Error() << endl;\n"
    save_str += "               return false;\n"
    save_str += "           }\n"
    save_str += "           tinyxml2::XMLElement* root = doc.FirstChildElement();\n"
    save_str += "           if (root == nullptr)\n"
    save_str += "           {\n"
    save_str += "               cerr << \"Failed to load file: No root element.\" << endl;\n"
    save_str += "               doc.Clear();\n"
    save_str += "               return false;\n"
    save_str += "           }\n"
    save_str += "           for (tinyxml2::XMLElement* elem = root->FirstChildElement(); elem != nullptr; elem = elem->NextSiblingElement())\n"
    save_str += "           {\n"
    save_str += "               "+filename+" data;\n"
    for col in range(0,len(key_list)):
        data_type = data_type_list[col]
        data_name = key_list[col]
        if data_type == Excel_Type.int.value:
            save_str += "               elem->QueryIntAttribute(\""+data_name+"\",&data."+data_name+");\n"
        elif data_type == Excel_Type.float.value:
            save_str += "               elem->QueryFloatAttribute(\"" + data_name + "\",&data." + data_name + ");\n"
        elif data_type == Excel_Type.string.value:
            save_str += "               data."+data_name+" = string(elem->Attribute(\""+data_name+"\"));\n"
        elif data_type == Excel_Type.bool.value:
            save_str += "               elem->QueryIntAttribute(\"" + data_name + "\",&data." + data_name + ");\n"
    save_str += "               _map[data."+key_list[UID_col]+"] = data;\n"
    save_str += "           }\n"
    save_str += "           doc.Clear();\n"
    save_str += "           return true;\n"
    save_str += "       }\n"
    save_str += "       "+filename+"* GetItem("+tran_dict[data_type_list[UID_col]]+" key)\n"
    save_str += "       {\n"
    save_str += "           Iterator iter = _map.find(key);\n"
    save_str += "           if(iter != _map.end())\n"
    save_str += "           {\n"
    save_str += "               return &iter->second;\n"
    save_str += "           }\n"
    save_str += "           return nullptr;\n"
    save_str += "       }\n"
    save_str += "       Map& GetMap()\n"
    save_str += "       {\n"
    save_str += "           return _map;\n"
    save_str += "       }\n"
    save_str += "    };\n"
    save_str += "    " + filename + "Parser* " + filename + "Parser::_ins = nullptr;\n"
    save_str += "}"
    #生成文件
    path = export_type_list["export_path"]
    filename = filename + "_Xml.h"
    OutFile(path, filename, save_str)

def ExportJSON(filename,key_list,data_type_list,final_value_list,export_type_list):
    save_str = "[\n"
    for row in range(0,len(final_value_list)):
        save_str += "{"
        for col in range(0,len(final_value_list[row])):
            if data_type_list[col] == Excel_Type.string.value:
                save_str += "\""+key_list[col]+"\":\""+str(final_value_list[row][col])+"\""
            else:
                save_str += "\""+key_list[col]+"\":"+str(final_value_list[row][col])
            if col <= (len(final_value_list[row])-2):
                save_str += ","
        save_str += "}"
        if row <= (len(final_value_list)-2):
            save_str += ",\n"
    save_str += "\n]"
    # 生成文件
    path = export_type_list["export_path"]
    filename = filename+".json"
    OutFile(path,filename,save_str)

def ExportJSONCPP(filename, key_list, data_type_list, export_type_list):
    save_str = ""
    tran_dict = type_compair[export_type_list["type"]]
    #导出头文件
    inc_list = type_include[export_type_list["type"]]
    for inc_str in inc_list:
        save_str += inc_str+"\n"
    #导出固定命名空间
    save_str += "namespace ExcelJson\n"
    save_str += "{\n"
    #导出结构struct
    save_str += "    struct "+filename+"\n"
    save_str += "    {\n"
    for key_i in range(0,len(key_list)):
        save_str += "        "+tran_dict[data_type_list[key_i]]+" "+key_list[key_i]+";\n"
    save_str += "    };\n"
    #导出解析class
    save_str += "    class " + filename + "Parser\n"
    save_str += "    {\n"
    #--Instance--
    save_str += "    private:\n"
    save_str += "       static "+filename+"Parser* _ins;\n"
    save_str += "    public:\n"
    save_str += "       static "+filename+"Parser& GetInstance()\n"
    save_str += "       {\n"
    save_str += "           if(!_ins)\n"
    save_str += "           {\n"
    save_str += "               _ins = new "+filename + "Parser();\n"
    save_str += "           }\n"
    save_str += "           return *_ins;\n"
    save_str += "       }\n"
    #--map--
    save_str += "   private:\n"
    save_str += "       typedef map<"+tran_dict[data_type_list[UID_col]]+","+filename+"> Map;\n"
    save_str += "       typedef map<" + tran_dict[data_type_list[UID_col]] + "," + filename + ">::iterator Iterator;\n"
    save_str += "       Map _map;\n"
    #--Load--
    save_str += "    public:\n"
    save_str += "       bool Load()\n"
    save_str += "       {\n"
    save_str += "           using namespace rapidjson;\n"
    save_str += "           FILE *fb = fopen(\""+export_type_list["import_path"]+filename+".json\",\"r+\");\n"
    save_str += "           if (fb == NULL)\n"
    save_str += "           {\n"
    save_str += "               cerr << \"open "+filename+".json failed. \"<< endl;\n"
    save_str += "               return false;\n"
    save_str += "           }\n"
    save_str += "           char buff[1024*16] = { 0 };\n"
    save_str += "           int len = fread(buff,1, 1024 * 16, fb);\n"
    save_str += "           fclose(fb);\n"
    save_str += "           string result;\n"
    save_str += "           if (len > 0)\n"
    save_str += "           {\n"
    save_str += "               result.append(buff, 0, len);\n "
    save_str += "           }\n"
    save_str += "           Document doc;\n"
    save_str += "           if (doc.Parse(result.c_str()).HasParseError())\n"
    save_str += "           {\n"
    save_str += "               cerr << \"parse error!\" << endl;\n"
    save_str += "               return false;\n"
    save_str += "           }\n"
    save_str += "           for (unsigned int row = 0; row < doc.Size(); ++row)\n"
    save_str += "           {\n"
    save_str += "               "+filename+" data;\n"
    save_str += "               const Value &item = doc[row];\n"
    for col in range(0,len(key_list)):
        data_type = data_type_list[col]
        data_name = key_list[col]
        if data_type == Excel_Type.int.value:
            save_str += "               data."+data_name+" = item[\""+data_name+"\"].GetInt();\n"
        elif data_type == Excel_Type.float.value:
            save_str += "               data." + data_name + " = item[\"" + data_name + "\"].GetFloat();\n"
        elif data_type == Excel_Type.string.value:
            save_str += "               data." + data_name + " = item[\"" + data_name + "\"].GetString();\n"
        elif data_type == Excel_Type.bool.value:
            save_str += "               data." + data_name + " = item[\"" + data_name + "\"].GetInt();\n"
    save_str += "               _map[data."+key_list[UID_col]+"] = data;\n"
    save_str += "           }\n"
    save_str += "           return true;\n"
    save_str += "       }\n"
    save_str += "       "+filename+"* GetItem("+tran_dict[data_type_list[UID_col]]+" key)\n"
    save_str += "       {\n"
    save_str += "           Iterator iter = _map.find(key);\n"
    save_str += "           if(iter != _map.end())\n"
    save_str += "           {\n"
    save_str += "               return &iter->second;\n"
    save_str += "           }\n"
    save_str += "           return nullptr;\n"
    save_str += "       }\n"
    save_str += "       Map& GetMap()\n"
    save_str += "       {\n"
    save_str += "           return _map;\n"
    save_str += "       }\n"
    save_str += "    };\n"
    save_str += "    "+filename+"Parser* "+filename+"Parser::_ins = nullptr;\n"
    save_str += "}"
    #生成文件
    path = export_type_list["export_path"]
    filename = filename + "_Json.h"
    OutFile(path, filename, save_str)




