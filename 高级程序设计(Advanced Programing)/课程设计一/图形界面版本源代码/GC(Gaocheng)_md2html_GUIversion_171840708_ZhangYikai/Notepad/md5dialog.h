#ifndef MD5DIALOG_H
#define MD5DIALOG_H

#include <QDialog>
#include <QCryptographicHash>
#include <QClipboard>


namespace Ui {
class MD5Dialog;
}

class MD5Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit MD5Dialog(QWidget *parent = 0);
    ~MD5Dialog();

private slots:
    void on_copyToClipboardButton_clicked();
    void generatemd5();

private:
    Ui::MD5Dialog *ui;
};

#endif // MD5DIALOG_H
