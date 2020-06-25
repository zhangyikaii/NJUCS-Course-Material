#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    initStatus();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::initStatus()
{
    //显示当前软件版本
    //1.通常注册表 ini等
    //2.IPC进程间通信 主要通过QProcess实现
    QString currentVersion = "0.0.1";
    ui->currentVersionLabel->setText(tr("Current Version : %1").arg(currentVersion));
    requestUpdatesInfo();

    // 初始化组件
    ui->progressBar->hide();
    ui->groupBox_2->hide();
    ui->downloadBtn->setEnabled(false);

    // 获取当前的时间戳，设置下载的临时文件名称
    QDateTime dateTime = QDateTime::currentDateTime();
    QString date = dateTime.toString("yyyy-MM-dd-hh-mm-ss-zzz");
    m_sFileName =  QString(QApplication::applicationDirPath() + "/%1.tmp").arg(date);
    qDebug() << m_sFileName;

}

//请求更新信息
void MainWindow::requestUpdatesInfo()
{
    QUrl url("http://doc.zhfsky.com/qt/notepad/update.json");
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(url);
    connect(manager, SIGNAL(finished(QNetworkReply*)), this, SLOT(parseUpdatesInfo(QNetworkReply*)));
    manager->get(request);

}
//解析更新信息
void MainWindow::parseUpdatesInfo(QNetworkReply* reply)
{
    QByteArray byteArray = reply->readAll();
    QJsonParseError jsonError;
    // 转化为 JSON 文档
    QJsonDocument doucment = QJsonDocument::fromJson(byteArray, &jsonError);
    if (!doucment.isNull() && (jsonError.error == QJsonParseError::NoError))
    {
        // 解析未发生错误
        if (doucment.isObject())
        {
            // JSON 文档为对象
            QJsonObject object = doucment.object();  // 转化为对象
            if (object.contains("version"))
            {
                // 包含指定的 key
                QJsonValue value = object.value("version");
                if (value.isString())
                    m_sLatestVersion = value.toString();

            }

            if (object.contains("download_url"))
            {
                QJsonValue value = object.value("download_url");
                if (value.isString())
                    m_sDownloadUrl = value.toString();

            }
            if (object.contains("update_log"))
            {
                QJsonValue value = object.value("update_log");
                if (value.isString())
                    m_sUpdateLog = value.toString();
            }

        }
    }

    // 更新组件
    if(!m_sLatestVersion.isEmpty())
        ui->latestVersionLabel->setText(tr("Latest Version : %1").arg(m_sLatestVersion));

    if(!m_sUpdateLog.isEmpty())
        ui->textEdit->setText(m_sUpdateLog);

    if(!m_sDownloadUrl.isEmpty())
        ui->downloadBtn->setEnabled(true);

}


//点击下载
void MainWindow::on_downloadBtn_clicked()
{
    m_url = QUrl(m_sDownloadUrl);
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request;
    request.setUrl(m_url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/zip");

    m_reply = manager->get(request);
    // 有新的数据可以读取
    connect(m_reply, SIGNAL(readyRead()), this, SLOT(httpReadyRead()));
    // 网络请求的下载进度更新
    connect(m_reply, SIGNAL(downloadProgress(qint64,qint64)), this, SLOT(updateDownlodProgress(qint64,qint64)));
    // 应答处理结束
    connect(m_reply, SIGNAL(finished()), this, SLOT(httpFinished()));
    // 开始计时
    m_tDownloadTime.start();
    m_nTime = 0;

    // 更新组件
    ui->groupBox_2->show();
    ui->downloadBtn->setEnabled(false);
    ui->progressBar->setValue(0);
    ui->progressBar->show();
    ui->groupBox_2->setTitle(tr("Downloading"));


}


//有新的数据可以读取
void MainWindow::httpReadyRead()
{
    //更新组件
    ui->fileNameLabel->setText(tr("File Name : %1").arg(m_url.fileName()));

    //写入文件
    QFile file(m_sFileName);
    if (file.open(QIODevice::Append))
        file.write(m_reply->readAll());
    file.close();

}

//网络请求的下载进度更新
void MainWindow::updateDownlodProgress(qint64 bytesReceived, qint64 bytesTotal)
{
    // 总时间
    int nTime = m_tDownloadTime.elapsed();
    // 本次下载所用时间
    nTime -= m_nTime;

    // 下载速度
    double dBytesSpeed = (bytesReceived * 1000.0) / nTime;
    double dSpeed = dBytesSpeed;

    //剩余时间
    qint64 leftBytes = (bytesTotal - bytesReceived);
    double dLeftTime = (leftBytes * 1.0) / dBytesSpeed;

    //更新组件信息
    ui->fileSizeLabel->setText(tr("File Size : %1").arg(size(bytesTotal)));
    ui->alreadDownloadLabel->setText(tr("Already Download : %1").arg(size(bytesReceived)));
    ui->timeLeftLabel->setText(tr("Time Left : %1").arg(timeFormat(qCeil(dLeftTime))));
    ui->speedLabel->setText(tr("Speed : %1").arg(speed(dSpeed)));

    ui->progressBar->setMaximum(bytesTotal);
    ui->progressBar->setValue(bytesReceived);

    // 获取上一次的时间
    m_nTime = nTime;

}


//下载完成
void MainWindow::httpFinished()
{
    // 获取响应的信息，状态码为200表示正常
    QVariant statusCode = m_reply->attribute(QNetworkRequest::HttpStatusCodeAttribute);

    // 无错误返回
    if (m_reply->error() == QNetworkReply::NoError)
    {
        // 重命名临时文件为真实文件名
        QFileInfo fileInfo(m_sFileName);
        QFileInfo newFileInfo = fileInfo.absolutePath() + m_url.fileName();
        QDir dir;
        if (dir.exists(fileInfo.absolutePath()))
        {
            if (newFileInfo.exists())
                newFileInfo.dir().remove(newFileInfo.fileName());
            QFile::rename(m_sFileName, newFileInfo.absoluteFilePath());
        }

        // 删除reply
        m_reply->deleteLater();
        m_reply = 0;


        // 更新组件
        ui->progressBar->hide();
        ui->downloadBtn->setEnabled(true);

        if(statusCode.toInt()==200){
            ui->groupBox_2->setTitle(tr("Download Complete"));
        }else{
            ui->groupBox_2->setTitle(tr("Download Failed"));
        }


        qDebug() << newFileInfo.absoluteFilePath();
        // 运行新版本软件进行安装

        QMessageBox box(this);
        box.setWindowTitle(tr("Update!"));
        box.setIcon(QMessageBox::Information);
        box.setText(tr("Download is done,Update ?"));
        QPushButton *yesBtn = box.addButton(tr("Yes"), QMessageBox::YesRole);
        QPushButton *noBtn = box.addButton(tr("No"), QMessageBox::NoRole);

        box.exec();
        QPushButton* clickedButton =(QPushButton*)box.clickedButton();

        if ( clickedButton== yesBtn){
            QString program =  newFileInfo.absoluteFilePath();
            QStringList arguments;
            QProcess *process = new QProcess(this);
            process->setProcessChannelMode(QProcess::SeparateChannels);
            process->setReadChannel(QProcess::StandardOutput);
            process->start(program, arguments, QIODevice::ReadWrite);
        }



    }
    else
    {
        QString strError = m_reply->errorString();
        QMessageBox::warning(this, tr("Download Error"), strError);
    }



}



// 字节转KB、MB、GB
QString MainWindow::size(qint64 bytes)
{
    QString strUnit;
    double dSize = bytes * 1.0;
    if (dSize <= 0)
    {
        dSize = 0.0;
    }
    else if (dSize < 1024)
    {
        strUnit = "Bytes";
    }
    else if (dSize < 1024 * 1024)
    {
        dSize /= 1024;
        strUnit = "KB";
    }
    else if (dSize < 1024 * 1024 * 1024)
    {
        dSize /= (1024 * 1024);
        strUnit = "MB";
    }
    else
    {
        dSize /= (1024 * 1024 * 1024);
        strUnit = "GB";
    }

    return QString("%1 %2").arg(QString::number(dSize, 'f', 2)).arg(strUnit);
}

// 速度转KB/S、MB/S、GB/S
QString MainWindow::speed(double speed)
{
    QString strUnit;
    if (speed <= 0)
    {
        speed = 0;
        strUnit = "Bytes/S";
    }
    else if (speed < 1024)
    {
        strUnit = "Bytes/S";
    }
    else if (speed < 1024 * 1024)
    {
        speed /= 1024;
        strUnit = "KB/S";
    }
    else if (speed < 1024 * 1024 * 1024)
    {
        speed /= (1024 * 1024);
        strUnit = "MB/S";
    }
    else
    {
        speed /= (1024 * 1024 * 1024);
        strUnit = "GB/S";
    }

    QString strSpeed = QString::number(speed, 'f', 2);
    return QString("%1 %2").arg(strSpeed).arg(strUnit);
}

// 秒转*d *h *m *s
QString MainWindow::timeFormat(int seconds)
{
    QString strValue;
    QString strSpacing(" ");
    if (seconds <= 0)
    {
        strValue = QString("%1s").arg(0);
    }
    else if (seconds < 60)
    {
        strValue = QString("%1s").arg(seconds);
    }
    else if (seconds < 60 * 60)
    {
        int nMinute = seconds / 60;
        int nSecond = seconds - nMinute * 60;

        strValue = QString("%1m").arg(nMinute);

        if (nSecond > 0)
            strValue += strSpacing + QString("%1s").arg(nSecond);
    }
    else if (seconds < 60 * 60 * 24)
    {
        int nHour = seconds / (60 * 60);
        int nMinute = (seconds - nHour * 60 * 60) / 60;
        int nSecond = seconds - nHour * 60 * 60 - nMinute * 60;

        strValue = QString("%1h").arg(nHour);

        if (nMinute > 0)
            strValue += strSpacing + QString("%1m").arg(nMinute);

        if (nSecond > 0)
            strValue += strSpacing + QString("%1s").arg(nSecond);
    }
    else
    {
        int nDay = seconds / (60 * 60 * 24);
        int nHour = (seconds - nDay * 60 * 60 * 24) / (60 * 60);
        int nMinute = (seconds - nDay * 60 * 60 * 24 - nHour * 60 * 60) / 60;
        int nSecond = seconds - nDay * 60 * 60 * 24 - nHour * 60 * 60 - nMinute * 60;

        strValue = QString("%1d").arg(nDay);

        if (nHour > 0)
            strValue += strSpacing + QString("%1h").arg(nHour);

        if (nMinute > 0)
            strValue += strSpacing + QString("%1m").arg(nMinute);

        if (nSecond > 0)
            strValue += strSpacing + QString("%1s").arg(nSecond);
    }

    return strValue;
}

