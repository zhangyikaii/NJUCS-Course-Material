#pragma once
#include "MdFile.h"
#include "HtmlFile.h"

class Admin
{
public:
    void Read2MdFile(string cont = "", string fName = "");
    void Md2Html();

private:
    MdFile mdf;
    HtmlFile htf;
};
