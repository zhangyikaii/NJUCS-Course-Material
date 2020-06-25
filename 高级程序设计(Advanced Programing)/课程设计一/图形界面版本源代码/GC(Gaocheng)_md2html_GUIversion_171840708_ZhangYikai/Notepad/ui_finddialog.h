/********************************************************************************
** Form generated from reading UI file 'finddialog.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FINDDIALOG_H
#define UI_FINDDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_FindDialog
{
public:
    QGridLayout *gridLayout;
    QTabWidget *tabWidget;
    QWidget *findTab;
    QLabel *targetLabel;
    QComboBox *comboBox;
    QPushButton *findNextOneButton;
    QPushButton *countButton;
    QPushButton *cancelButton;
    QGroupBox *groupBox;
    QCheckBox *findReverseCk;
    QCheckBox *matchWholeWordCk;
    QCheckBox *matchCaseCk;
    QPushButton *showAllMatchesButon;
    QWidget *replaceTab;
    QPushButton *findNextOneButton_2;
    QComboBox *comboBox_2;
    QLabel *targetLabel_2;
    QGroupBox *groupBox_2;
    QCheckBox *findReverseCk_2;
    QCheckBox *matchWholeWordCk_2;
    QCheckBox *matchCaseCk_2;
    QLabel *replaceLabel;
    QComboBox *comboBox_3;
    QPushButton *cancelButton_2;
    QPushButton *replaceButton;
    QPushButton *replaceAllButton;
    QWidget *fileFindTab;
    QLabel *targetLabel_3;
    QLabel *replaceLabel_2;
    QComboBox *comboBox_4;
    QComboBox *comboBox_5;
    QLabel *fileTypeLabel;
    QComboBox *comboBox_6;
    QLabel *directoryLabel;
    QComboBox *comboBox_7;
    QToolButton *toolButton;
    QPushButton *findAllButton;
    QLabel *statusLabel;

    void setupUi(QDialog *FindDialog)
    {
        if (FindDialog->objectName().isEmpty())
            FindDialog->setObjectName(QStringLiteral("FindDialog"));
        FindDialog->resize(593, 358);
        QFont font;
        font.setFamily(QStringLiteral("Microsoft JhengHei"));
        FindDialog->setFont(font);
        gridLayout = new QGridLayout(FindDialog);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        tabWidget = new QTabWidget(FindDialog);
        tabWidget->setObjectName(QStringLiteral("tabWidget"));
        QFont font1;
        font1.setFamily(QStringLiteral("Microsoft JhengHei UI"));
        tabWidget->setFont(font1);
        findTab = new QWidget();
        findTab->setObjectName(QStringLiteral("findTab"));
        targetLabel = new QLabel(findTab);
        targetLabel->setObjectName(QStringLiteral("targetLabel"));
        targetLabel->setGeometry(QRect(10, 20, 91, 31));
        comboBox = new QComboBox(findTab);
        comboBox->setObjectName(QStringLiteral("comboBox"));
        comboBox->setGeometry(QRect(110, 20, 281, 31));
        comboBox->setEditable(true);
        findNextOneButton = new QPushButton(findTab);
        findNextOneButton->setObjectName(QStringLiteral("findNextOneButton"));
        findNextOneButton->setGeometry(QRect(410, 20, 151, 31));
        countButton = new QPushButton(findTab);
        countButton->setObjectName(QStringLiteral("countButton"));
        countButton->setGeometry(QRect(410, 70, 151, 31));
        cancelButton = new QPushButton(findTab);
        cancelButton->setObjectName(QStringLiteral("cancelButton"));
        cancelButton->setGeometry(QRect(410, 170, 151, 31));
        groupBox = new QGroupBox(findTab);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        groupBox->setGeometry(QRect(10, 130, 191, 111));
        findReverseCk = new QCheckBox(groupBox);
        findReverseCk->setObjectName(QStringLiteral("findReverseCk"));
        findReverseCk->setGeometry(QRect(10, 20, 71, 21));
        matchWholeWordCk = new QCheckBox(groupBox);
        matchWholeWordCk->setObjectName(QStringLiteral("matchWholeWordCk"));
        matchWholeWordCk->setGeometry(QRect(10, 50, 151, 21));
        matchCaseCk = new QCheckBox(groupBox);
        matchCaseCk->setObjectName(QStringLiteral("matchCaseCk"));
        matchCaseCk->setGeometry(QRect(10, 80, 91, 21));
        showAllMatchesButon = new QPushButton(findTab);
        showAllMatchesButon->setObjectName(QStringLiteral("showAllMatchesButon"));
        showAllMatchesButon->setGeometry(QRect(410, 120, 151, 31));
        tabWidget->addTab(findTab, QString());
        replaceTab = new QWidget();
        replaceTab->setObjectName(QStringLiteral("replaceTab"));
        findNextOneButton_2 = new QPushButton(replaceTab);
        findNextOneButton_2->setObjectName(QStringLiteral("findNextOneButton_2"));
        findNextOneButton_2->setGeometry(QRect(410, 20, 151, 31));
        comboBox_2 = new QComboBox(replaceTab);
        comboBox_2->setObjectName(QStringLiteral("comboBox_2"));
        comboBox_2->setGeometry(QRect(110, 20, 281, 31));
        comboBox_2->setEditable(true);
        targetLabel_2 = new QLabel(replaceTab);
        targetLabel_2->setObjectName(QStringLiteral("targetLabel_2"));
        targetLabel_2->setGeometry(QRect(10, 20, 91, 31));
        groupBox_2 = new QGroupBox(replaceTab);
        groupBox_2->setObjectName(QStringLiteral("groupBox_2"));
        groupBox_2->setGeometry(QRect(10, 130, 191, 111));
        findReverseCk_2 = new QCheckBox(groupBox_2);
        findReverseCk_2->setObjectName(QStringLiteral("findReverseCk_2"));
        findReverseCk_2->setGeometry(QRect(10, 20, 71, 21));
        matchWholeWordCk_2 = new QCheckBox(groupBox_2);
        matchWholeWordCk_2->setObjectName(QStringLiteral("matchWholeWordCk_2"));
        matchWholeWordCk_2->setGeometry(QRect(10, 50, 151, 21));
        matchCaseCk_2 = new QCheckBox(groupBox_2);
        matchCaseCk_2->setObjectName(QStringLiteral("matchCaseCk_2"));
        matchCaseCk_2->setGeometry(QRect(10, 80, 91, 21));
        replaceLabel = new QLabel(replaceTab);
        replaceLabel->setObjectName(QStringLiteral("replaceLabel"));
        replaceLabel->setGeometry(QRect(10, 70, 91, 31));
        comboBox_3 = new QComboBox(replaceTab);
        comboBox_3->setObjectName(QStringLiteral("comboBox_3"));
        comboBox_3->setGeometry(QRect(110, 70, 281, 31));
        comboBox_3->setEditable(true);
        cancelButton_2 = new QPushButton(replaceTab);
        cancelButton_2->setObjectName(QStringLiteral("cancelButton_2"));
        cancelButton_2->setGeometry(QRect(410, 170, 151, 31));
        replaceButton = new QPushButton(replaceTab);
        replaceButton->setObjectName(QStringLiteral("replaceButton"));
        replaceButton->setGeometry(QRect(410, 70, 151, 31));
        replaceAllButton = new QPushButton(replaceTab);
        replaceAllButton->setObjectName(QStringLiteral("replaceAllButton"));
        replaceAllButton->setGeometry(QRect(410, 120, 151, 31));
        tabWidget->addTab(replaceTab, QString());
        fileFindTab = new QWidget();
        fileFindTab->setObjectName(QStringLiteral("fileFindTab"));
        targetLabel_3 = new QLabel(fileFindTab);
        targetLabel_3->setObjectName(QStringLiteral("targetLabel_3"));
        targetLabel_3->setGeometry(QRect(10, 20, 91, 31));
        replaceLabel_2 = new QLabel(fileFindTab);
        replaceLabel_2->setObjectName(QStringLiteral("replaceLabel_2"));
        replaceLabel_2->setGeometry(QRect(10, 70, 91, 31));
        comboBox_4 = new QComboBox(fileFindTab);
        comboBox_4->setObjectName(QStringLiteral("comboBox_4"));
        comboBox_4->setGeometry(QRect(110, 20, 281, 31));
        comboBox_4->setEditable(true);
        comboBox_5 = new QComboBox(fileFindTab);
        comboBox_5->setObjectName(QStringLiteral("comboBox_5"));
        comboBox_5->setGeometry(QRect(110, 70, 281, 31));
        comboBox_5->setEditable(true);
        fileTypeLabel = new QLabel(fileFindTab);
        fileTypeLabel->setObjectName(QStringLiteral("fileTypeLabel"));
        fileTypeLabel->setGeometry(QRect(10, 120, 91, 31));
        comboBox_6 = new QComboBox(fileFindTab);
        comboBox_6->setObjectName(QStringLiteral("comboBox_6"));
        comboBox_6->setGeometry(QRect(110, 120, 281, 31));
        comboBox_6->setEditable(true);
        directoryLabel = new QLabel(fileFindTab);
        directoryLabel->setObjectName(QStringLiteral("directoryLabel"));
        directoryLabel->setGeometry(QRect(10, 170, 91, 31));
        comboBox_7 = new QComboBox(fileFindTab);
        comboBox_7->setObjectName(QStringLiteral("comboBox_7"));
        comboBox_7->setGeometry(QRect(110, 170, 281, 31));
        comboBox_7->setEditable(true);
        toolButton = new QToolButton(fileFindTab);
        toolButton->setObjectName(QStringLiteral("toolButton"));
        toolButton->setGeometry(QRect(400, 170, 51, 31));
        findAllButton = new QPushButton(fileFindTab);
        findAllButton->setObjectName(QStringLiteral("findAllButton"));
        findAllButton->setGeometry(QRect(410, 20, 151, 31));
        tabWidget->addTab(fileFindTab, QString());

        gridLayout->addWidget(tabWidget, 0, 0, 1, 1);

        statusLabel = new QLabel(FindDialog);
        statusLabel->setObjectName(QStringLiteral("statusLabel"));
        statusLabel->setFont(font);

        gridLayout->addWidget(statusLabel, 1, 0, 2, 1);


        retranslateUi(FindDialog);

        tabWidget->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(FindDialog);
    } // setupUi

    void retranslateUi(QDialog *FindDialog)
    {
        FindDialog->setWindowTitle(QApplication::translate("FindDialog", "Find", nullptr));
        tabWidget->setProperty("title", QVariant(QApplication::translate("FindDialog", "SSS", nullptr)));
#ifndef QT_NO_TOOLTIP
        findTab->setToolTip(QApplication::translate("FindDialog", "<html><head/><body><p>Find String</p></body></html>", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_STATUSTIP
        findTab->setStatusTip(QString());
#endif // QT_NO_STATUSTIP
#ifndef QT_NO_ACCESSIBILITY
        findTab->setAccessibleName(QApplication::translate("FindDialog", "Find Find", nullptr));
#endif // QT_NO_ACCESSIBILITY
        targetLabel->setText(QApplication::translate("FindDialog", "Target to Find", nullptr));
        findNextOneButton->setText(QApplication::translate("FindDialog", "Find Next One", nullptr));
        countButton->setText(QApplication::translate("FindDialog", "Counts", nullptr));
        cancelButton->setText(QApplication::translate("FindDialog", "Cancel", nullptr));
        groupBox->setTitle(QApplication::translate("FindDialog", "SettingGroupBox", nullptr));
        findReverseCk->setText(QApplication::translate("FindDialog", "Reverse", nullptr));
        matchWholeWordCk->setText(QApplication::translate("FindDialog", "Match Whole Word", nullptr));
        matchCaseCk->setText(QApplication::translate("FindDialog", "Match Case", nullptr));
        showAllMatchesButon->setText(QApplication::translate("FindDialog", "Show All Matches", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(findTab), QApplication::translate("FindDialog", "Find", nullptr));
        findNextOneButton_2->setText(QApplication::translate("FindDialog", "Find Next One", nullptr));
        targetLabel_2->setText(QApplication::translate("FindDialog", "Target to Find", nullptr));
        groupBox_2->setTitle(QApplication::translate("FindDialog", "SettingGroupBox", nullptr));
        findReverseCk_2->setText(QApplication::translate("FindDialog", "Reverse", nullptr));
        matchWholeWordCk_2->setText(QApplication::translate("FindDialog", "Match Whole Word", nullptr));
        matchCaseCk_2->setText(QApplication::translate("FindDialog", "Match Case", nullptr));
        replaceLabel->setText(QApplication::translate("FindDialog", "Replace To", nullptr));
        cancelButton_2->setText(QApplication::translate("FindDialog", "Cancel", nullptr));
        replaceButton->setText(QApplication::translate("FindDialog", "Replace", nullptr));
        replaceAllButton->setText(QApplication::translate("FindDialog", "Replace All", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(replaceTab), QApplication::translate("FindDialog", "Replace", nullptr));
        targetLabel_3->setText(QApplication::translate("FindDialog", "Target to Find", nullptr));
        replaceLabel_2->setText(QApplication::translate("FindDialog", "Replace To", nullptr));
        fileTypeLabel->setText(QApplication::translate("FindDialog", "File Type", nullptr));
        directoryLabel->setText(QApplication::translate("FindDialog", "Directory", nullptr));
        toolButton->setText(QApplication::translate("FindDialog", "...", nullptr));
        findAllButton->setText(QApplication::translate("FindDialog", "Find All", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(fileFindTab), QApplication::translate("FindDialog", "File Find", nullptr));
        statusLabel->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class FindDialog: public Ui_FindDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FINDDIALOG_H
