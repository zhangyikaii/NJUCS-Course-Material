#include "statics.h"

Statics::Statics()
{

}

Statics::Statics(QSettings *settings)
{
    setting = settings;
}

void Statics::setSetting(QSettings *settings)
{
    setting = settings;
}

void Statics::usesInfo(){
    setting->beginGroup("Statics");
    QString useTime = setting->value("usetime", QVariant(0)).toString();//使用软件的总时长 分钟
    QString startSoftwareTimes = setting->value("startsoftwaretimes", QVariant(0)).toString();// 打开软件的总次数
    setting->endGroup();

    // 画图
    //QFont font("Times New Roman");

    //![1]
    QBarSet *set0 = new QBarSet("Jane");
    QBarSet *set1 = new QBarSet("John");
    QBarSet *set2 = new QBarSet("Axel");
    QBarSet *set3 = new QBarSet("Mary");
    QBarSet *set4 = new QBarSet("Samantha");



    *set0 << 1 << 2 << 3 << 4 << 5 << 6;
    *set1 << 5 << 0 << 0 << 4 << 0 << 7;
    *set2 << 3 << 5 << 8 << 13 << 8 << 5;
    *set3 << 5 << 6 << 7 << 3 << 4 << 5;
    *set4 << 9 << 7 << 5 << 3 << 1 << 2;
//![1]

//![2]
    QBarSeries *series = new QBarSeries();
    series->append(set0);
    series->append(set1);
    series->append(set2);
    series->append(set3);
    series->append(set4);

//![2]

//![3]
    QChart *chart = new QChart();
    chart->addSeries(series);
    chart->setTitle("Simple barchart example");

    chart->setAnimationOptions(QChart::SeriesAnimations);
//![3]

//![4]
    QStringList categories;
    categories << "Jan" << "Feb" << "Mar" << "Apr" << "May" << "Jun";
    QBarCategoryAxis *axis = new QBarCategoryAxis();
    axis->append(categories);
    chart->createDefaultAxes();
    chart->setAxisX(axis, series);
//![4]

//![5]
    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);
//![5]

//![6]
    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
//![6]

//![7]
    chartView->resize(420, 300);
    chartView->setWindowTitle(QObject::tr("Statics"));
    chartView->show();
//![7]
}
