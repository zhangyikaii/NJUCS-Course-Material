/********************************************************************************
** Form generated from reading UI file 'notepad.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_NOTEPAD_H
#define UI_NOTEPAD_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Notepad
{
public:
    QAction *actionOpen;
    QAction *actionSave;
    QAction *actionPrint;
    QAction *actionExit;
    QAction *actionNew;
    QAction *actionFont;
    QAction *actionUndo;
    QAction *actionCut;
    QAction *actionCopy;
    QAction *actionPaste;
    QAction *actionDelete;
    QAction *actionFind;
    QAction *actionReplace;
    QAction *actionSave_as;
    QAction *actionMD5;
    QAction *actionUpdate;
    QAction *actionAbout;
    QAction *actionBlog;
    QAction *actionDonate;
    QAction *actionBase64_Encode;
    QAction *actionBase64_Decode;
    QAction *actionURL_Encode;
    QAction *actionURL_Decode;
    QAction *actionConvert_to_Upper;
    QAction *actionConver_to_Lower;
    QAction *actionFirst_Letter_Upper;
    QAction *actionConvert_UL;
    QAction *actionEntrypt_File;
    QAction *actionDecrypt_File;
    QAction *actionReboot;
    QAction *actionLoginout;
    QAction *actionInfo;
    QAction *actionStatics;
    QAction *actionOptions;
    QAction *actionHide;
    QAction *actionGCmd2Html;
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QMenuBar *menuBar;
    QMenu *menuFile;
    QMenu *menuType;
    QMenu *menu;
    QMenu *menuSetting;
    QMenu *menuHelp;
    QMenu *menuUser;
    QMenu *menuGCmd2html;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;
    QToolBar *toolBar;

    void setupUi(QMainWindow *Notepad)
    {
        if (Notepad->objectName().isEmpty())
            Notepad->setObjectName(QStringLiteral("Notepad"));
        Notepad->resize(670, 368);
        QFont font;
        font.setFamily(QStringLiteral("Microsoft YaHei"));
        Notepad->setFont(font);
        QIcon icon;
        icon.addFile(QStringLiteral(":/images/favicon.ico"), QSize(), QIcon::Normal, QIcon::Off);
        Notepad->setWindowIcon(icon);
        actionOpen = new QAction(Notepad);
        actionOpen->setObjectName(QStringLiteral("actionOpen"));
        QIcon icon1;
        icon1.addFile(QStringLiteral(":/images/images/open.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionOpen->setIcon(icon1);
        actionSave = new QAction(Notepad);
        actionSave->setObjectName(QStringLiteral("actionSave"));
        QIcon icon2;
        icon2.addFile(QStringLiteral(":/images/images/save.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionSave->setIcon(icon2);
        actionPrint = new QAction(Notepad);
        actionPrint->setObjectName(QStringLiteral("actionPrint"));
        QIcon icon3;
        icon3.addFile(QStringLiteral(":/images/images/print.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionPrint->setIcon(icon3);
        actionExit = new QAction(Notepad);
        actionExit->setObjectName(QStringLiteral("actionExit"));
        QIcon icon4;
        icon4.addFile(QStringLiteral(":/images/images/close.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionExit->setIcon(icon4);
        actionNew = new QAction(Notepad);
        actionNew->setObjectName(QStringLiteral("actionNew"));
        QIcon icon5;
        icon5.addFile(QStringLiteral(":/images/images/new.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionNew->setIcon(icon5);
        actionFont = new QAction(Notepad);
        actionFont->setObjectName(QStringLiteral("actionFont"));
        QIcon icon6;
        icon6.addFile(QStringLiteral(":/images/images/font.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionFont->setIcon(icon6);
        actionUndo = new QAction(Notepad);
        actionUndo->setObjectName(QStringLiteral("actionUndo"));
        QIcon icon7;
        icon7.addFile(QStringLiteral(":/images/images/undo.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionUndo->setIcon(icon7);
        actionCut = new QAction(Notepad);
        actionCut->setObjectName(QStringLiteral("actionCut"));
        QIcon icon8;
        icon8.addFile(QStringLiteral(":/images/images/cut.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionCut->setIcon(icon8);
        actionCopy = new QAction(Notepad);
        actionCopy->setObjectName(QStringLiteral("actionCopy"));
        QIcon icon9;
        icon9.addFile(QStringLiteral(":/images/images/copy.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionCopy->setIcon(icon9);
        actionPaste = new QAction(Notepad);
        actionPaste->setObjectName(QStringLiteral("actionPaste"));
        QIcon icon10;
        icon10.addFile(QStringLiteral(":/images/images/paste.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionPaste->setIcon(icon10);
        actionDelete = new QAction(Notepad);
        actionDelete->setObjectName(QStringLiteral("actionDelete"));
        QIcon icon11;
        icon11.addFile(QStringLiteral(":/images/images/delete.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDelete->setIcon(icon11);
        actionFind = new QAction(Notepad);
        actionFind->setObjectName(QStringLiteral("actionFind"));
        QIcon icon12;
        icon12.addFile(QStringLiteral(":/images/images/find.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionFind->setIcon(icon12);
        actionReplace = new QAction(Notepad);
        actionReplace->setObjectName(QStringLiteral("actionReplace"));
        QIcon icon13;
        icon13.addFile(QStringLiteral(":/images/images/replace.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionReplace->setIcon(icon13);
        actionSave_as = new QAction(Notepad);
        actionSave_as->setObjectName(QStringLiteral("actionSave_as"));
        QIcon icon14;
        icon14.addFile(QStringLiteral(":/images/images/save-as.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionSave_as->setIcon(icon14);
        actionMD5 = new QAction(Notepad);
        actionMD5->setObjectName(QStringLiteral("actionMD5"));
        actionUpdate = new QAction(Notepad);
        actionUpdate->setObjectName(QStringLiteral("actionUpdate"));
        QIcon icon15;
        icon15.addFile(QStringLiteral(":/images/images/update.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionUpdate->setIcon(icon15);
        actionAbout = new QAction(Notepad);
        actionAbout->setObjectName(QStringLiteral("actionAbout"));
        QIcon icon16;
        icon16.addFile(QStringLiteral(":/images/images/about.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionAbout->setIcon(icon16);
        actionBlog = new QAction(Notepad);
        actionBlog->setObjectName(QStringLiteral("actionBlog"));
        QIcon icon17;
        icon17.addFile(QStringLiteral(":/images/images/blog.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionBlog->setIcon(icon17);
        actionDonate = new QAction(Notepad);
        actionDonate->setObjectName(QStringLiteral("actionDonate"));
        QIcon icon18;
        icon18.addFile(QStringLiteral(":/images/images/donate.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDonate->setIcon(icon18);
        actionBase64_Encode = new QAction(Notepad);
        actionBase64_Encode->setObjectName(QStringLiteral("actionBase64_Encode"));
        actionBase64_Decode = new QAction(Notepad);
        actionBase64_Decode->setObjectName(QStringLiteral("actionBase64_Decode"));
        actionURL_Encode = new QAction(Notepad);
        actionURL_Encode->setObjectName(QStringLiteral("actionURL_Encode"));
        actionURL_Decode = new QAction(Notepad);
        actionURL_Decode->setObjectName(QStringLiteral("actionURL_Decode"));
        actionConvert_to_Upper = new QAction(Notepad);
        actionConvert_to_Upper->setObjectName(QStringLiteral("actionConvert_to_Upper"));
        actionConver_to_Lower = new QAction(Notepad);
        actionConver_to_Lower->setObjectName(QStringLiteral("actionConver_to_Lower"));
        actionFirst_Letter_Upper = new QAction(Notepad);
        actionFirst_Letter_Upper->setObjectName(QStringLiteral("actionFirst_Letter_Upper"));
        actionConvert_UL = new QAction(Notepad);
        actionConvert_UL->setObjectName(QStringLiteral("actionConvert_UL"));
        actionEntrypt_File = new QAction(Notepad);
        actionEntrypt_File->setObjectName(QStringLiteral("actionEntrypt_File"));
        actionDecrypt_File = new QAction(Notepad);
        actionDecrypt_File->setObjectName(QStringLiteral("actionDecrypt_File"));
        actionReboot = new QAction(Notepad);
        actionReboot->setObjectName(QStringLiteral("actionReboot"));
        QIcon icon19;
        icon19.addFile(QStringLiteral(":/images/images/reboot .png"), QSize(), QIcon::Normal, QIcon::Off);
        actionReboot->setIcon(icon19);
        actionLoginout = new QAction(Notepad);
        actionLoginout->setObjectName(QStringLiteral("actionLoginout"));
        QIcon icon20;
        icon20.addFile(QStringLiteral(":/images/images/loginout.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionLoginout->setIcon(icon20);
        actionInfo = new QAction(Notepad);
        actionInfo->setObjectName(QStringLiteral("actionInfo"));
        QIcon icon21;
        icon21.addFile(QStringLiteral(":/images/images/user.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionInfo->setIcon(icon21);
        actionStatics = new QAction(Notepad);
        actionStatics->setObjectName(QStringLiteral("actionStatics"));
        QIcon icon22;
        icon22.addFile(QStringLiteral(":/images/images/statics.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionStatics->setIcon(icon22);
        actionOptions = new QAction(Notepad);
        actionOptions->setObjectName(QStringLiteral("actionOptions"));
        actionHide = new QAction(Notepad);
        actionHide->setObjectName(QStringLiteral("actionHide"));
        QIcon icon23;
        icon23.addFile(QStringLiteral(":/images/images/hide.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionHide->setIcon(icon23);
        actionGCmd2Html = new QAction(Notepad);
        actionGCmd2Html->setObjectName(QStringLiteral("actionGCmd2Html"));
        actionGCmd2Html->setIcon(icon21);
        centralWidget = new QWidget(Notepad);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        Notepad->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(Notepad);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 670, 18));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QStringLiteral("menuFile"));
        menuType = new QMenu(menuBar);
        menuType->setObjectName(QStringLiteral("menuType"));
        menu = new QMenu(menuBar);
        menu->setObjectName(QStringLiteral("menu"));
        menuSetting = new QMenu(menuBar);
        menuSetting->setObjectName(QStringLiteral("menuSetting"));
        menuHelp = new QMenu(menuBar);
        menuHelp->setObjectName(QStringLiteral("menuHelp"));
        menuUser = new QMenu(menuBar);
        menuUser->setObjectName(QStringLiteral("menuUser"));
        menuGCmd2html = new QMenu(menuBar);
        menuGCmd2html->setObjectName(QStringLiteral("menuGCmd2html"));
        Notepad->setMenuBar(menuBar);
        mainToolBar = new QToolBar(Notepad);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        Notepad->addToolBar(Qt::RightToolBarArea, mainToolBar);
        statusBar = new QStatusBar(Notepad);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        Notepad->setStatusBar(statusBar);
        toolBar = new QToolBar(Notepad);
        toolBar->setObjectName(QStringLiteral("toolBar"));
        Notepad->addToolBar(Qt::TopToolBarArea, toolBar);

        menuBar->addAction(menuGCmd2html->menuAction());
        menuBar->addAction(menuFile->menuAction());
        menuBar->addAction(menu->menuAction());
        menuBar->addAction(menuType->menuAction());
        menuBar->addAction(menuSetting->menuAction());
        menuBar->addAction(menuHelp->menuAction());
        menuBar->addAction(menuUser->menuAction());
        menuFile->addAction(actionNew);
        menuFile->addAction(actionOpen);
        menuFile->addAction(actionSave);
        menuFile->addAction(actionSave_as);
        menuFile->addSeparator();
        menuFile->addAction(actionPrint);
        menuFile->addSeparator();
        menuFile->addAction(actionExit);
        menuType->addAction(actionFont);
        menu->addAction(actionUndo);
        menu->addSeparator();
        menu->addAction(actionCut);
        menu->addAction(actionCopy);
        menu->addAction(actionPaste);
        menu->addAction(actionDelete);
        menu->addSeparator();
        menu->addAction(actionFind);
        menu->addAction(actionReplace);
        menuSetting->addAction(actionOptions);
        menuHelp->addAction(actionBlog);
        menuHelp->addAction(actionReboot);
        menuHelp->addAction(actionStatics);
        menuHelp->addAction(actionHide);
        menuUser->addAction(actionInfo);
        menuUser->addSeparator();
        menuGCmd2html->addAction(actionGCmd2Html);

        retranslateUi(Notepad);

        QMetaObject::connectSlotsByName(Notepad);
    } // setupUi

    void retranslateUi(QMainWindow *Notepad)
    {
        Notepad->setWindowTitle(QApplication::translate("Notepad", "Notepad", nullptr));
        actionOpen->setText(QApplication::translate("Notepad", "Open(&O)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionOpen->setShortcut(QApplication::translate("Notepad", "Ctrl+O", nullptr));
#endif // QT_NO_SHORTCUT
        actionSave->setText(QApplication::translate("Notepad", "Save(&S)", nullptr));
#ifndef QT_NO_TOOLTIP
        actionSave->setToolTip(QApplication::translate("Notepad", "Save(S)", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionSave->setShortcut(QApplication::translate("Notepad", "Ctrl+S", nullptr));
#endif // QT_NO_SHORTCUT
        actionPrint->setText(QApplication::translate("Notepad", "Print(&P)", nullptr));
#ifndef QT_NO_TOOLTIP
        actionPrint->setToolTip(QApplication::translate("Notepad", "Print(P)", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionPrint->setShortcut(QApplication::translate("Notepad", "Ctrl+P", nullptr));
#endif // QT_NO_SHORTCUT
        actionExit->setText(QApplication::translate("Notepad", "Exit", nullptr));
        actionNew->setText(QApplication::translate("Notepad", "New(&N)", nullptr));
#ifndef QT_NO_TOOLTIP
        actionNew->setToolTip(QApplication::translate("Notepad", "New(N)", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionNew->setShortcut(QApplication::translate("Notepad", "Ctrl+N", nullptr));
#endif // QT_NO_SHORTCUT
        actionFont->setText(QApplication::translate("Notepad", "Font", nullptr));
        actionUndo->setText(QApplication::translate("Notepad", "Undo(&U)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionUndo->setShortcut(QApplication::translate("Notepad", "Ctrl+Z", nullptr));
#endif // QT_NO_SHORTCUT
        actionCut->setText(QApplication::translate("Notepad", "Cut(&T)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionCut->setShortcut(QApplication::translate("Notepad", "Ctrl+X", nullptr));
#endif // QT_NO_SHORTCUT
        actionCopy->setText(QApplication::translate("Notepad", "Copy(&C)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionCopy->setShortcut(QApplication::translate("Notepad", "Ctrl+C", nullptr));
#endif // QT_NO_SHORTCUT
        actionPaste->setText(QApplication::translate("Notepad", "Paste(&P)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionPaste->setShortcut(QApplication::translate("Notepad", "Ctrl+V", nullptr));
#endif // QT_NO_SHORTCUT
        actionDelete->setText(QApplication::translate("Notepad", "Delete(&L)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionDelete->setShortcut(QApplication::translate("Notepad", "Del", nullptr));
#endif // QT_NO_SHORTCUT
        actionFind->setText(QApplication::translate("Notepad", "Find(&F)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionFind->setShortcut(QApplication::translate("Notepad", "Ctrl+F", nullptr));
#endif // QT_NO_SHORTCUT
        actionReplace->setText(QApplication::translate("Notepad", "Replace(&R)", nullptr));
#ifndef QT_NO_SHORTCUT
        actionReplace->setShortcut(QApplication::translate("Notepad", "Ctrl+H", nullptr));
#endif // QT_NO_SHORTCUT
        actionSave_as->setText(QApplication::translate("Notepad", "Save as(&A)", nullptr));
        actionMD5->setText(QApplication::translate("Notepad", "MD5", nullptr));
        actionUpdate->setText(QApplication::translate("Notepad", "Update", nullptr));
        actionAbout->setText(QApplication::translate("Notepad", "About", nullptr));
        actionBlog->setText(QApplication::translate("Notepad", "My GitHub", nullptr));
        actionDonate->setText(QApplication::translate("Notepad", "Donate", nullptr));
        actionBase64_Encode->setText(QApplication::translate("Notepad", "Base64 Encode", nullptr));
        actionBase64_Decode->setText(QApplication::translate("Notepad", "Base64 Decode", nullptr));
        actionURL_Encode->setText(QApplication::translate("Notepad", "URL Encode", nullptr));
        actionURL_Decode->setText(QApplication::translate("Notepad", "URL Decode", nullptr));
        actionConvert_to_Upper->setText(QApplication::translate("Notepad", "Convert to Upper", nullptr));
        actionConver_to_Lower->setText(QApplication::translate("Notepad", "Conver to Lower", nullptr));
        actionFirst_Letter_Upper->setText(QApplication::translate("Notepad", "First Letter Upper", nullptr));
        actionConvert_UL->setText(QApplication::translate("Notepad", "Convert UL", nullptr));
        actionEntrypt_File->setText(QApplication::translate("Notepad", "Entrypt File", nullptr));
        actionDecrypt_File->setText(QApplication::translate("Notepad", "Decrypt File", nullptr));
        actionReboot->setText(QApplication::translate("Notepad", "Reboot", nullptr));
        actionLoginout->setText(QApplication::translate("Notepad", "Loginout", nullptr));
        actionInfo->setText(QApplication::translate("Notepad", "Info", nullptr));
        actionStatics->setText(QApplication::translate("Notepad", "Statics", nullptr));
        actionOptions->setText(QApplication::translate("Notepad", "Options", nullptr));
        actionHide->setText(QApplication::translate("Notepad", "Hide", nullptr));
        actionGCmd2Html->setText(QApplication::translate("Notepad", "GCmd2Html", nullptr));
#ifndef QT_NO_SHORTCUT
        actionGCmd2Html->setShortcut(QApplication::translate("Notepad", "Ctrl+G", nullptr));
#endif // QT_NO_SHORTCUT
        menuFile->setTitle(QApplication::translate("Notepad", "File", nullptr));
        menuType->setTitle(QApplication::translate("Notepad", "Type", nullptr));
        menu->setTitle(QApplication::translate("Notepad", "Edit", nullptr));
        menuSetting->setTitle(QApplication::translate("Notepad", "Setting", nullptr));
        menuHelp->setTitle(QApplication::translate("Notepad", "Help", nullptr));
        menuUser->setTitle(QApplication::translate("Notepad", "User", nullptr));
        menuGCmd2html->setTitle(QApplication::translate("Notepad", "GCmd2html", nullptr));
        toolBar->setWindowTitle(QApplication::translate("Notepad", "toolBar", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Notepad: public Ui_Notepad {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_NOTEPAD_H
