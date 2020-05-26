#pragma once
#include <string>
#include <iostream>
#include <map>
#include "../ServerEngine/ServerEngine.h"
#include "../ServerEngine/tinyxml/tinyxml2.h"
using namespace std;
namespace ExcelXml
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
           tinyxml2::XMLDocument doc;
           if (doc.LoadFile("../resource/excel/Scene.xml") != tinyxml2::XMLError::XML_SUCCESS)
           {
               cerr << doc.Error() << endl;
               return false;
           }
           tinyxml2::XMLElement* root = doc.FirstChildElement();
           if (root == nullptr)
           {
               cerr << "Failed to load file: No root element." << endl;
               doc.Clear();
               return false;
           }
           for (tinyxml2::XMLElement* elem = root->FirstChildElement(); elem != nullptr; elem = elem->NextSiblingElement())
           {
               Scene data;
               elem->QueryIntAttribute("Gid",&data.Gid);
               data.MeshFile = string(elem->Attribute("MeshFile"));
               _map[data.Gid] = data;
           }
           doc.Clear();
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