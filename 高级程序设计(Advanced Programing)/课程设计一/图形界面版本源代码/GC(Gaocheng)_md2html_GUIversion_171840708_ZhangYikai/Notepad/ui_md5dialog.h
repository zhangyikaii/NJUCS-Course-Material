/********************************************************************************
** Form generated from reading UI file 'md5dialog.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MD5DIALOG_H
#define UI_MD5DIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_MD5Dialog
{
public:
    QHBoxLayout *horizontalLayout;
    QVBoxLayout *verticalLayout;
    QPlainTextEdit *inputTextEdit;
    QPlainTextEdit *outputTextEdit;
    QPushButton *copyToClipboardButton;

    void setupUi(QDialog *MD5Dialog)
    {
        if (MD5Dialog->objectName().isEmpty())
            MD5Dialog->setObjectName(QStringLiteral("MD5Dialog"));
        MD5Dialog->resize(420, 304);
        QFont font;
        font.setFamily(QStringLiteral("Microsoft YaHei"));
        MD5Dialog->setFont(font);
        horizontalLayout = new QHBoxLayout(MD5Dialog);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        inputTextEdit = new QPlainTextEdit(MD5Dialog);
        inputTextEdit->setObjectName(QStringLiteral("inputTextEdit"));

        verticalLayout->addWidget(inputTextEdit);

        outputTextEdit = new QPlainTextEdit(MD5Dialog);
        outputTextEdit->setObjectName(QStringLiteral("outputTextEdit"));
        outputTextEdit->setStyleSheet(QStringLiteral("background-color: rgb(213, 213, 213);"));
        outputTextEdit->setReadOnly(true);
        outputTextEdit->setBackgroundVisible(false);

        verticalLayout->addWidget(outputTextEdit);


        horizontalLayout->addLayout(verticalLayout);

        copyToClipboardButton = new QPushButton(MD5Dialog);
        copyToClipboardButton->setObjectName(QStringLiteral("copyToClipboardButton"));
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Maximum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(copyToClipboardButton->sizePolicy().hasHeightForWidth());
        copyToClipboardButton->setSizePolicy(sizePolicy);
        copyToClipboardButton->setMinimumSize(QSize(110, 50));

        horizontalLayout->addWidget(copyToClipboardButton);


        retranslateUi(MD5Dialog);

        QMetaObject::connectSlotsByName(MD5Dialog);
    } // setupUi

    void retranslateUi(QDialog *MD5Dialog)
    {
        MD5Dialog->setWindowTitle(QApplication::translate("MD5Dialog", "Generate MD5 value", nullptr));
        copyToClipboardButton->setText(QApplication::translate("MD5Dialog", "Copy to Clipboard", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MD5Dialog: public Ui_MD5Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MD5DIALOG_H
