#include "Admin.h"

void Admin::Read2MdFile(string cont, string fname) {
    mdf.CreateMdFile(cont, fname);
}

void Admin::Md2Html() {
    htf.CreateHtmlFile(this->mdf);
}
