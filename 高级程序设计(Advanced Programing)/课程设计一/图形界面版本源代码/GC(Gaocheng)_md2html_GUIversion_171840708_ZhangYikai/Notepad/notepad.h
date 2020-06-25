#ifndef NOTEPAD_H
#define NOTEPAD_H

#include <QMainWindow>
#include <QFileDialog>
#include <QMessageBox>
#include <QFile>
#include <QTextStream>
#include <QFontDialog>
#include <QCloseEvent>
#include <QLineEdit>
#include <QDialog>
#include <QPushButton>
#include <QLabel>
#include <QDesktopServices>
#include <QTextCursor>
#include <QDebug>
#include <QTextEdit>
#include <QPainter>
#include <QPlainTextEdit>
#include <QClipboard>
#include <QSettings>
#include <QPrinter>
#include <QPrintDialog>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QProcess>
#include <QTimer>
#include <QDesktopWidget>



#include "highlighter.h"
#include "codeeditor.h"
#include "user.h"
#include "setting.h"
#include "traymenu.h"
#include "statics.h"


namespace Ui {
class Notepad;
}


class Notepad : public QMainWindow
{
    Q_OBJECT

public:
    explicit Notepad(QWidget *parent = 0);
    ~Notepad();
    CodeEditor *codeEditor;

protected:
    void openFindReplaceDialog(QString flag);

    void showStatusBar();

    void requestAboutContent(QTextEdit *text);

    void updateAboutWidet(QTextEdit *text, QString content);

    void showTipsMessage();
protected slots:

    void updateMenuActionStatus();

    void updateSetting();

    void tipsMessageMove();
    void tipsMessageStay();
    void tipsMessageClose();

private slots:
    void on_actionNew_triggered();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();
    void on_actionSave_as_triggered();
    void on_actionPrint_triggered();
    void on_actionFont_triggered();
    void on_actionExit_triggered();
    void on_actionUndo_triggered();
    void on_actionCut_triggered();
    void on_actionCopy_triggered();
    void on_actionPaste_triggered();
    void on_actionDelete_triggered();
    void on_actionFind_triggered();
    void on_actionMD5_triggered();
    void on_actionBlog_triggered();
    void on_actionBase64_Encode_triggered();
    void on_actionBase64_Decode_triggered();
    void on_actionURL_Encode_triggered();
    void on_actionURL_Decode_triggered();
    void on_actionConvert_to_Upper_triggered();
    void on_actionConver_to_Lower_triggered();
    void on_actionFirst_Letter_Upper_triggered();
    void on_actionConvert_UL_triggered();
    void on_actionReplace_triggered();
    void on_actionAbout_triggered();
    void on_actionUpdate_triggered();
    void on_actionReboot_triggered();
    void on_actionDonate_triggered();
    void on_actionStatics_triggered();
    void on_actionInfo_triggered();
    void on_actionOptions_triggered();

    void on_actionJSON_triggered();

    void on_actionHide_triggered();


    void on_actionGCmd2Html_triggered();

private:
    Ui::Notepad *ui;
    QString CurrentFile;
    bool isUntitled;
    bool hasSaved;

    // 状态栏
    QLabel *statusLabel;

    //剪贴板
    QClipboard *clip;

    //Setting
    QSettings *setting;

    //语法高亮
    Highlighter *highlighter;

    // 右下角提示
    QTimer *m_pShowTimer;
    QTimer *m_pStayTimer;
    QTimer *m_pCloseTimer;
    QPoint m_point;
    double m_dTransparent; //透明度
    int m_nDesktopHeight;
    QDialog *tipsDlg;

    bool loadFile(const QString &fileName);
    bool saveFile(const QString &fileName);
    bool saveFileAs();
    bool save();
    bool saveBeforeAction();
    void closeEvent(QCloseEvent *event); // 关闭事件
    void initStatus();
    void readSetting();
    void initWindow(QWidget *widget);
};


#endif // NOTEPAD_H
