#include "notepad.h"
#include <QApplication>
#include <QTranslator>
#include "commonhelper.h"


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    // 翻译
    QTranslator translator;
    translator.load(":/language/NotepadI18N_zh_CN.qm");
    a.installTranslator(&translator);

    // 主窗口
    Notepad w;
    w.show();
    return a.exec();
}
