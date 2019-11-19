/********************************************************************************
** Form generated from reading UI file 'jsondialog.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_JSONDIALOG_H
#define UI_JSONDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>

QT_BEGIN_NAMESPACE

class Ui_JsonDialog
{
public:

    void setupUi(QDialog *JsonDialog)
    {
        if (JsonDialog->objectName().isEmpty())
            JsonDialog->setObjectName(QStringLiteral("JsonDialog"));
        JsonDialog->resize(710, 501);

        retranslateUi(JsonDialog);

        QMetaObject::connectSlotsByName(JsonDialog);
    } // setupUi

    void retranslateUi(QDialog *JsonDialog)
    {
        JsonDialog->setWindowTitle(QApplication::translate("JsonDialog", "Dialog", nullptr));
    } // retranslateUi

};

namespace Ui {
    class JsonDialog: public Ui_JsonDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_JSONDIALOG_H
