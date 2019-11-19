#include "mainwindow.h"
#include <QApplication>
#include <QSystemSemaphore>
#include <QSharedMemory>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QSystemSemaphore sema("notepad",1,QSystemSemaphore::Open);
    sema.acquire();// 在临界区操作共享内存

    QSharedMemory mem("notepad_update");// 全局对象名
    if (!mem.create(1))// 如果全局对象以存在则退出
    {
        QMessageBox::information(0, QObject::tr("Warning"),QObject::tr("Another process is running !"));
        sema.release();
        return 0;
    }
    sema.release();

    MainWindow w;
    w.setWindowTitle("Notepad Update");
    w.show();

    return a.exec();
}
