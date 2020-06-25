#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QUrl>
#include <QDebug>
#include <QJsonParseError>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QFileInfo>
#include <QFile>
#include <QTime>
#include <QtMath>
#include <QDir>
#include <QMessageBox>
#include <QProcess>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

protected:
    void initStatus();

    QString timeFormat(int seconds);
    QString speed(double speed);
    QString size(qint64 bytes);
protected slots:

    void parseUpdatesInfo(QNetworkReply *reply);
    void requestUpdatesInfo();

    void updateDownlodProgress(qint64 bytesReceived, qint64 bytesTotal);
    void httpReadyRead();
    void httpFinished();

private slots:
    void on_downloadBtn_clicked();

private:
    Ui::MainWindow *ui;


    QString m_sLatestVersion;
    QString m_sDownloadUrl;
    QString m_sUpdateLog;


    //下载
    QNetworkReply *m_reply;
    QString m_sFileName;//临时文件名
    QUrl m_url;

    //QNetworkAccessManager *manager;



    //QFile *m_file;  //文件指针

    QTime m_tDownloadTime;
    int m_nTime;

};

#endif // MAINWINDOW_H
