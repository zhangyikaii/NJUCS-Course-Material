#ifndef FINDDIALOG_H
#define FINDDIALOG_H

#include <QDialog>
#include <QPlainTextEdit>
#include <QMessageBox>
#include <QTextCursor>
#include <QDebug>
#include <QComboBox>

namespace Ui {
class FindDialog;
}

class FindDialog : public QDialog
{
    Q_OBJECT

public:
    explicit FindDialog(QWidget *parent = 0, QString flag = "find");
    QPlainTextEdit *docmainEdit;
    ~FindDialog();

private slots:
    void on_findNextOneButton_clicked();

    void on_countButton_clicked();

    void on_showAllMatchesButon_clicked();

    void on_cancelButton_clicked();

    void on_findNextOneButton_2_clicked();

    void on_replaceButton_clicked();

    void on_replaceAllButton_clicked();

    void on_cancelButton_2_clicked();

private:
    Ui::FindDialog *ui;
    void updateCombox(QComboBox *box);

};

#endif // FINDDIALOG_H
