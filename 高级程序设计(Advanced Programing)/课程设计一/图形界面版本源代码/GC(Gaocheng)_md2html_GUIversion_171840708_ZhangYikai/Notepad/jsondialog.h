#ifndef JSONDIALOG_H
#define JSONDIALOG_H

#include <QDialog>

namespace Ui {
class JsonDialog;
}

class JsonDialog : public QDialog
{
    Q_OBJECT

public:
    explicit JsonDialog(QWidget *parent = 0);
    ~JsonDialog();

private:
    Ui::JsonDialog *ui;
};

#endif // JSONDIALOG_H
