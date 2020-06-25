#include "notepad.h"
#include "ui_notepad.h"
#include "md5dialog.h"
#include "finddialog.h"
#include "globalmacro.h"

#include "Admin.h"
#include <QDebug>



Notepad::Notepad(QWidget *parent) : QMainWindow(parent), ui(new Ui::Notepad)
{
    //初始化窗口
    initWindow(this);
    ui->setupUi(this);

    codeEditor = new CodeEditor(this);
    codeEditor->setFont(QFont("",16));
    this->setCentralWidget(codeEditor);

    // 初始化文件为未保存状态
    isUntitled = true;
    hasSaved = false;
    CurrentFile = "Untitled.md";

    //语法高亮 C++
    highlighter = new Highlighter(codeEditor->document());

    // 状态栏
    showStatusBar();


    initStatus();
}

Notepad::~Notepad()
{
    delete ui;
}

/***打开程序的初始化工作***/
void Notepad::initStatus()
{
    /*Menu action的初始化*/
    ui->actionUndo->setDisabled(true);
    ui->actionCut->setDisabled(true);
    ui->actionCopy->setDisabled(true);
    ui->actionDelete->setDisabled(true);
    ui->actionPaste->setDisabled(true);

    //实例化clipboard对象
    clip = QApplication::clipboard();

    //信号的链接
    connect(clip, SIGNAL(dataChanged()), this, SLOT(updateMenuActionStatus()));
    connect(codeEditor, SIGNAL(undoAvailable(bool)), this, SLOT(updateMenuActionStatus()));
    connect(codeEditor, SIGNAL(selectionChanged()), this, SLOT(updateMenuActionStatus()));

    //右下角提示
    m_pShowTimer = new QTimer(this);
    m_pStayTimer = new QTimer(this);
    m_pCloseTimer = new QTimer(this);
    m_dTransparent = 1.0;
    connect(m_pShowTimer, SIGNAL(timeout()), this, SLOT(tipsMessageMove()));
    connect(m_pStayTimer, SIGNAL(timeout()), this, SLOT(tipsMessageStay()));
    connect(m_pCloseTimer, SIGNAL(timeout()), this, SLOT(tipsMessageClose()));

}

/***初始化窗口信息***/
void Notepad::initWindow(QWidget *widget)
{
    /*Setting的初始化*/
    //setting = new QSettings("The Future", "NotePad");//windows下写入注册表
    setting = new QSettings("config.ini", QSettings::IniFormat);//ini文件

    setting->beginGroup("mainWindow");
    //窗口大小
    QSize winSize = setting->value("winSize", QSize(800, 1000)).toSize();
    widget->resize(winSize);

    bool maximSize = setting->value("maximSize", false).toBool();
    if(maximSize)
        widget->setWindowState(Qt::WindowMaximized);
    //位置
    QPoint winPos = setting->value("winPos").toPoint();
    widget->move(winPos);

    setting->endGroup();
}

/****读取Setting**/
void Notepad::readSetting()
{

}

/***SLOT:更新Setting***/
void Notepad::updateSetting()
{
    setting->beginGroup("mainWindow");
    setting->setValue("maximSize", this->isMaximized());
    setting->setValue("winSize", this->size());
    setting->setValue("winPos", this->pos());
    setting->endGroup();
}

/***状态栏***/
void Notepad::showStatusBar()
{
    // 正常状态信息
    statusLabel = new QLabel();
    statusLabel->setMinimumSize(150,20);
    statusLabel->setFrameShape(QFrame::WinPanel);
    statusLabel->setFrameShadow(QFrame::Sunken);
    statusLabel->setText(tr("Thank you, GaoCheng TA bro."));
    ui->statusBar->addWidget(statusLabel);
    // 永久状态信息
    QLabel *permanentLabel = new QLabel(this);
    permanentLabel->setFrameStyle(QFrame::Box | QFrame::Sunken);
    permanentLabel->setText(tr("<a href=\"https://github.com/ZhangYikaii\">GitHub</a>"));
    permanentLabel->setTextFormat(Qt::RichText);
    permanentLabel->setOpenExternalLinks(true);
    ui->statusBar->addPermanentWidget(permanentLabel);
}

/***加载文件***/
bool Notepad::loadFile(const QString &fileName)
{
    QFile file(fileName); // 新建QFile对象
    if (!file.open(QFile::ReadOnly | QFile::Text))
    {
       QMessageBox::warning(this, tr("GCNotepad"), tr("Can't read file %1:\n%2.").arg(fileName).arg(file.errorString()));
       return false; // 只读方式打开文件，出错则提示，并返回false
    }
    QTextStream in(&file); // 新建文本流对象
    // 设置鼠标状态
    QApplication::setOverrideCursor(Qt::WaitCursor);
    // 读取文件的全部文本内容，并添加到编辑器中
    codeEditor->setPlainText(in.readAll());
    // 恢复鼠标状态
    QApplication::restoreOverrideCursor();
    // 设置当前文件
    CurrentFile = QFileInfo(fileName).canonicalFilePath();
    // 设置窗口标题
    setWindowTitle(CurrentFile);
    file.close();
    isUntitled = false;
    return true;
}

/***在执行action之前检测当前文档是否已经保存***/
bool Notepad::saveBeforeAction()
{
    // 当前文档被更改
    if(codeEditor->document()->isModified() && !hasSaved)
    {
        QMessageBox box(this);
        box.setWindowTitle(tr("Warnging"));
        box.setIcon(QMessageBox::Warning);
        box.setText(tr("Save the changes to\r") + CurrentFile + "?");
        QPushButton *yesBtn = box.addButton(tr("Yes"), QMessageBox::YesRole);
        QPushButton *noBtn = box.addButton(tr("No"), QMessageBox::NoRole);
        QPushButton *cancelBtn = box.addButton(tr("Cancel"), QMessageBox::RejectRole);
        box.exec();
        QPushButton* clickedButton =(QPushButton*)box.clickedButton();
        if ( clickedButton== yesBtn)
            return save(); // 保存
        else if (clickedButton == noBtn)
            return true; //不保存 直接返回true
        else if (clickedButton == cancelBtn)
            return false;// 什么也不做
    }
    // 如果文档没有被更改，则直接返回true
    return true;
}

/***保存文件***/
bool Notepad::save()
{
    if(isUntitled) // 文档以前没有保存过
    {
        return saveFileAs();
    }else{
        return saveFile(CurrentFile);
    }
}

/***文件另存为***/
bool Notepad::saveFileAs()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("Save as"), CurrentFile, tr("Document(*.md)"));
    if(fileName.isEmpty())
    {
        return false;
    }else{
        return saveFile(fileName);
    }
}

bool Notepad::saveFile(const QString &fileName)
{
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QFile::Text))
    {
        QMessageBox::warning(this, tr("GCNotepad"), tr("Cant't write file %1：/n %2").arg(fileName).arg(file.errorString()));
        return false;
    }
    QTextStream out(&file);
    // 鼠标指针变为等待状态
    QApplication::setOverrideCursor(Qt::WaitCursor);
    QString text = codeEditor->toPlainText();
    out << text;
    file.flush();
    file.close();
    // 鼠标指针恢复原来的状态
    QApplication::restoreOverrideCursor();
    isUntitled = false;
    // 获得文件的标准路径
    CurrentFile = QFileInfo(fileName).canonicalFilePath();
    // 设置窗口标题
    setWindowTitle(CurrentFile);
    hasSaved = true;
    return true;

}

/***直接关闭窗口事件处理***/
void Notepad::closeEvent(QCloseEvent *event)
{
    //更新Setting
    updateSetting();

    if(saveBeforeAction())
    {
        event->accept();
    }else{
        event->ignore();
    }
}

/***SLOT:新建***/
void Notepad::on_actionNew_triggered()
{
    if(saveBeforeAction())
    {
        CurrentFile = "Untitled.md";
        // 设置窗口标题
        setWindowTitle(CurrentFile);
        codeEditor->setPlainText("");
        // ui->textEdit->clear();
    }


}

/***SLOT:打开***/
void Notepad::on_actionOpen_triggered()
{
    if(saveBeforeAction())
    {
        QString fileName = QFileDialog::getOpenFileName(this, tr("Open the file"), tr(""), tr("Document(*.md)"));
        if(!fileName.isEmpty())
        {
            loadFile(fileName);
        }
    }
}

/***SLOT:保存***/
void Notepad::on_actionSave_triggered()
{
    save();
}

/***SLOT:另存为***/
void Notepad::on_actionSave_as_triggered()
{
    saveFileAs();
}

/***SLOT:打印***/
void Notepad::on_actionPrint_triggered()
{
    QPrinter printer;
    //创建一个QPrintDialog对象，参数为QPrinter对象
    QPrintDialog printDialog(&printer, this);
    //判断打印对话框显示后用户是否单击“打印”,打印--则相关打印属性将可以通过创建QPrintDialog
    //对象时,使用的QPrinter对象获得;单击取消，则不执行后续的打印操作
    if (printDialog.exec ())
    {
        //获得QTextEdit对象的文档
        QTextDocument *doc = codeEditor->document();
        //打印
        doc->print (&printer);
    }
}

/***SLOT:字体***/
void Notepad::on_actionFont_triggered()
{
    bool fontSelected;
    QFont font = QFontDialog::getFont(&fontSelected, this);
    if (fontSelected) {
        codeEditor->setFont(font);
    }
}

/***SLOT:退出***/
void Notepad::on_actionExit_triggered()
{
    if(saveBeforeAction()){
        //更新Setting
        updateSetting();
        // qApp是指向应用程序的全局指针
        qApp->quit();
    }
}

/***SLOT:撤销***/
void Notepad::on_actionUndo_triggered()
{
    codeEditor->undo();
}

/***SLOT:剪切***/
void Notepad::on_actionCut_triggered()
{
    codeEditor->cut();
}

/***SLOT:复制***/
void Notepad::on_actionCopy_triggered()
{
    codeEditor->copy();
}

/***SLOT:粘贴***/
void Notepad::on_actionPaste_triggered()
{
    codeEditor->paste();
}

/***SLOT:删除***/
void Notepad::on_actionDelete_triggered()
{
    codeEditor->cut();
}

/***:查找和替换***/
void Notepad::openFindReplaceDialog(QString flag)
{
    FindDialog *dlg = new FindDialog(this, flag);
    dlg->docmainEdit = codeEditor;
    dlg->show();
}

/***SLOT:查找***/
void Notepad::on_actionFind_triggered()
{
    openFindReplaceDialog("find");
}

/***SLOT:替换***/
void Notepad::on_actionReplace_triggered()
{
    openFindReplaceDialog("replace");
}

/***SLOT:MD5***/
void Notepad::on_actionMD5_triggered()
{
    MD5Dialog *dlg = new MD5Dialog(this);
    dlg->show();
}

/***SLOT:博客***/
void Notepad::on_actionBlog_triggered()
{
    QDesktopServices::openUrl(QUrl(tr("https://github.com/ZhangYikaii")));
}

/***SLOT:Base64 Encode***/
void Notepad::on_actionBase64_Encode_triggered()
{
    QByteArray input;
    input.append(codeEditor->toPlainText());
    QString output(input.toBase64());
    codeEditor->setPlainText(output);
}

/***SLOT:Base64 Decode***/
void Notepad::on_actionBase64_Decode_triggered()
{
    QByteArray input;
    input.append(codeEditor->toPlainText());
    QString output(QByteArray::fromBase64(input));
    codeEditor->setPlainText(output);
}

void Notepad::on_actionURL_Encode_triggered()
{

}

void Notepad::on_actionURL_Decode_triggered()
{

}

/***SLOT:转换为大写***/
void Notepad::on_actionConvert_to_Upper_triggered()
{
    // 当前cursor对象
    QTextCursor cursor = codeEditor->textCursor();
    // 获取选择的文本
    QString text = cursor.selectedText();
    // 将选中文本全部转换为大写
    text = text.toUpper();
    // 删除选择的文本
    cursor.removeSelectedText();
    // 插入大写后的文本
    cursor.insertText(text);
    // 设置光标对象
    codeEditor->setTextCursor(cursor);

}

/***SLOT:转换为小写***/
void Notepad::on_actionConver_to_Lower_triggered()
{
    // 当前cursor对象
    QTextCursor cursor = codeEditor->textCursor();
    // 获取选择的文本
    QString text = cursor.selectedText();
    // 将选中文本全部转换为小写
    text = text.toLower();
    // 删除选择的文本
    cursor.removeSelectedText();
    // 插入小写后的文本
    cursor.insertText(text);
    // 设置光标对象
    codeEditor->setTextCursor(cursor);

}

/***SLOT:首字母大写***/
void Notepad::on_actionFirst_Letter_Upper_triggered()
{
    // 当前cursor对象
    QTextCursor cursor = codeEditor->textCursor();
    // 获取选择的文本
    QString text = cursor.selectedText();
    // 将选中文本全部转换为小写
    text = text.toLower();
    // 将选中文本的每个单词的首字母转换为大写
    QStringList parts = text.split(QRegExp("\\b")); // 每个Item 包括 单词 空白 符号
    for (int i = 0; i < parts.size(); ++i)
    {
        QString item = parts[i];
        if(!item.isEmpty()){
            parts[i].replace(0, 1, parts[i][0].toUpper());// 首字母大写
        }
    }

    QString output = parts.join("");// 拼接
    // 删除选择的文本
    cursor.removeSelectedText();
    // 插入大写后的文本
    cursor.insertText(output);
    // 设置光标对象
    codeEditor->setTextCursor(cursor);
}

/***SLOT:大小写相互转换***/
void Notepad::on_actionConvert_UL_triggered()
{
    // 当前cursor对象
    QTextCursor cursor = codeEditor->textCursor();
    // 获取选择的文本
    QString text = cursor.selectedText();

    for(int i=0; i<text.size();i++){
        // 选中英语字母
        if(text[i].isLetter()){
            if(text[i].isLower()){
                // 该字母小写 将其转换为大写
                text[i] = text[i].toUpper();
            }else if(text[i].isUpper()){
                // 该字母大写 将其转换为小写
                text[i] = text[i].toLower();
            }

        }

    }
    // 删除选择的文本
    cursor.removeSelectedText();
    // 插入大写后的文本
    cursor.insertText(text);
    // 设置光标对象
    codeEditor->setTextCursor(cursor);
}

/***SLOT:更新Menu Action状态***/
void Notepad::updateMenuActionStatus()
{
    if(codeEditor->isUndoRedoEnabled())
    {
        ui->actionUndo->setEnabled(true);
    }else{
        ui->actionUndo->setDisabled(true);
    }

    if(codeEditor->textCursor().hasSelection())
    {
        ui->actionCopy->setEnabled(true);
        ui->actionDelete->setEnabled(true);
        ui->actionCut->setEnabled(true);
    }else{
        ui->actionCopy->setDisabled(true);
        ui->actionDelete->setDisabled(true);
        ui->actionCut->setDisabled(true);
    }

    //剪贴板
    if(!clip->text().isEmpty()){
        ui->actionPaste->setEnabled(true);
    }else{
        ui->actionPaste->setDisabled(true);
    }
}

void Notepad::on_actionAbout_triggered()
{
    //创建dialog对象
    QDialog *aboutDlg = new QDialog(this);
    aboutDlg->setWindowTitle(tr("About Notepad"));
    aboutDlg->resize(QSize(500,300));
    //dialog的主布局
    QGridLayout *mainLayout = new QGridLayout(aboutDlg);


    // 软件介绍文字
    QHBoxLayout *layout = new QHBoxLayout(aboutDlg);
    QTextEdit *text = new QTextEdit(aboutDlg);
    text->setReadOnly(true);
    text->setFont(QFont("Microsoft Yahei"));

    // 异步请求
    requestAboutContent(text);


    //about qt
    QPushButton *btn = new QPushButton(tr("About Qt"), aboutDlg);
    connect(btn, SIGNAL(clicked(bool)), qApp, SLOT(aboutQt()));

    layout->addWidget(text);
    layout->addWidget(btn);

    mainLayout->addLayout(layout, 0, 0, 2, 5);

    aboutDlg->exec();



}


void Notepad::requestAboutContent(QTextEdit *text)
{

}

void Notepad::updateAboutWidet(QTextEdit *text, QString content)
{

    text->setText(content);
}


/***SLOT:软件检查更新***/
void Notepad::on_actionUpdate_triggered()
{
}


/***SLOT:重启软件***/
void Notepad::on_actionReboot_triggered()
{
    QString program = QApplication::applicationFilePath();
    QStringList arguments = QApplication::arguments();
    QString workingDirectory = QDir::currentPath();
    QProcess::startDetached(program, arguments, workingDirectory);
    QApplication::exit();

}

/***SLOT:捐赠***/
void Notepad::on_actionDonate_triggered()
{

}


void Notepad::showTipsMessage()
{
    QDesktopWidget *desktop = QApplication::desktop();
    //获取可用桌面大小
    QRect rect = desktop->availableGeometry();
    // 屏幕的高度
    // int screenHeight = desktop->screenGeometry().height();
    // 可用桌面的高度
    m_nDesktopHeight = desktop->availableGeometry().height();
    // 任务栏的高度
    // int taskBarHeight = screenHeight - m_nDesktopHeight ;


    //实例化Tips窗体控件
    tipsDlg = new QDialog();
    tipsDlg->setWindowTitle(tr("Tips Window"));
    QHBoxLayout *lay = new QHBoxLayout(tipsDlg);
    QTextEdit *text = new QTextEdit(tipsDlg);
    text->setText(tr("Statamic is different than other Content Management Systems like Wordpress, Drupal, or Craft CMS in many important and powerful ways, but the most obvious is we removed the MySQL database. It's for the greater good."));
    lay->addWidget(text);

    tipsDlg->show();

    // Tips窗体的左上角点位置
    m_point.setX(rect.width() - tipsDlg->frameGeometry().width());
    m_point.setY(rect.height() - tipsDlg->frameGeometry().height());
    // 将Tips窗体移至指定位置
    tipsDlg->move(m_point.x(), m_point.y());

    //显示开始计时
    m_pShowTimer->start(3);

    //当点击窗体时显示为不透明 或者鼠标进入tips窗体时显示为不透明 m_pStayTimer 重新计时

}

/***SLOT:移动Tips窗体***/
void Notepad::tipsMessageMove()
{
    // 向上移动
    m_nDesktopHeight--;
    // x不变 向上移动
    tipsDlg->move(m_point.x(), m_nDesktopHeight);
    if (m_nDesktopHeight <= m_point.y())
    {
        m_pShowTimer->stop();//显示结束计时
        m_pStayTimer->start(1000);// 停留开始计时
    }
}

void Notepad::tipsMessageStay()
{
    // 停留结束计时
    m_pStayTimer->stop();
    // 关闭开始计时
    m_pCloseTimer->start(100);
}

void Notepad::tipsMessageClose()
{
    m_dTransparent -= 0.01;
    if (m_dTransparent <= 0.0)
    {
        // 关闭停止计时
        m_pCloseTimer->stop();
        // 关闭Tips窗体
        tipsDlg->close();
    }
    else
    {
        tipsDlg->setWindowOpacity(m_dTransparent);
    }
}

/***SLOT:软件使用统计****/
void Notepad::on_actionStatics_triggered()
{
    Statics *statics = new Statics;
    statics->setSetting(setting);
    statics->usesInfo();


}

void Notepad::on_actionInfo_triggered()
{
    User *user = new User(this);
    user->show();
}

void Notepad::on_actionOptions_triggered()
{
    Setting *setting = new Setting(this);
    setting->show();
}

void Notepad::on_actionJSON_triggered()
{
}

void Notepad::on_actionHide_triggered()
{
    TrayMenu *traymenu = new TrayMenu(this);
    traymenu->trayIcon->show();

    hide();
}



void Notepad::on_actionGCmd2Html_triggered()
{
    Admin adm;
    QString fileName = QFileDialog::getSaveFileName(this, tr("Save as"), CurrentFile, tr("Document(*.html)"));
    if(fileName.isEmpty()) {
        return;
    }
    else {
       // 转换成Html并保存
       QFile file(fileName);
       if (!file.open(QIODevice::WriteOnly | QFile::Text)) {
           QMessageBox::warning(this, tr("GCNotepad"), tr("Cant't write file %1：/n %2").arg(fileName).arg(file.errorString()));
           return;
       }
       QTextStream out(&file);
       // 鼠标指针变为等待状态
       QApplication::setOverrideCursor(Qt::WaitCursor);

       // mdCont是当前窗口里面的md格式文本.
       string mdCont = codeEditor->toPlainText().toStdString();

       // 通过流写入文件.
       // out << text;
       file.flush();
       file.close();
       // 鼠标指针恢复原来的状态
       QApplication::restoreOverrideCursor();
       isUntitled = false;
       // 获得文件的标准路径
       CurrentFile = QFileInfo(fileName).canonicalFilePath();

       string fName = CurrentFile.toStdString();

       adm.Read2MdFile(mdCont, fName);
       adm.Md2Html();

       // 设置窗口标题
       setWindowTitle(CurrentFile);
       hasSaved = true;
       return;

       // return saveFile(fileName);
   }
}
