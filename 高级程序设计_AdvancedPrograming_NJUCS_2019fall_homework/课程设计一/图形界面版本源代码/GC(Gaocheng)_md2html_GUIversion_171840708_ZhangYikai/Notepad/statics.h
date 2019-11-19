#ifndef STATICS_H
#define STATICS_H

#include <QObject>
#include <QWidget>
#include <QSettings>
#include <QtCharts>


class Statics
{

public:
    Statics();
    Statics(QSettings *settings);
    void usesInfo();
    void setSetting(QSettings *settings);
private:
    QSettings *setting;
};

#endif // STATICS_H
