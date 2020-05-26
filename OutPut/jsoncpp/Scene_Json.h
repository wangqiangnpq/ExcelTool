#pragma once
#include <string>
#include <map>
#include <stdio.h>
#include "../ServerEngine/ServerEngine.h"
#include "../ServerEngine/rapidjson/rapidjson.h"
#include "../ServerEngine/rapidjson/document.h"
using namespace std;
namespace ExcelJson
{
    struct Scene
    {
        INT32 Gid;
        string MeshFile;
    };
    class SceneParser
    {
    private:
       static SceneParser* _ins;
    public:
       static SceneParser& GetInstance()
       {
           if(!_ins)
           {
               _ins = new SceneParser();
           }
           return *_ins;
       }
   private:
       typedef map<INT32,Scene> Map;
       typedef map<INT32,Scene>::iterator Iterator;
       Map _map;
    public:
       bool Load()
       {
           using namespace rapidjson;
           FILE *fb = fopen("../resource/excel/Scene.json","r+");
           if (fb == NULL)
           {
               cerr << "open Scene.json failed. "<< endl;
               return false;
           }
           char buff[1024*16] = { 0 };
           int len = fread(buff,1, 1024 * 16, fb);
           fclose(fb);
           string result;
           if (len > 0)
           {
               result.append(buff, 0, len);
            }
           Document doc;
           if (doc.Parse(result.c_str()).HasParseError())
           {
               cerr << "parse error!" << endl;
               return false;
           }
           for (unsigned int row = 0; row < doc.Size(); ++row)
           {
               Scene data;
               const Value &item = doc[row];
               data.Gid = item["Gid"].GetInt();
               data.MeshFile = item["MeshFile"].GetString();
               _map[data.Gid] = data;
           }
           return true;
       }
       Scene* GetItem(INT32 key)
       {
           Iterator iter = _map.find(key);
           if(iter != _map.end())
           {
               return &iter->second;
           }
           return nullptr;
       }
       Map& GetMap()
       {
           return _map;
       }
    };
    SceneParser* SceneParser::_ins = nullptr;
}