#include "jsondialog.h"
#include "ui_jsondialog.h"

JsonDialog::JsonDialog(QWidget *parent) : QDialog(parent), ui(new Ui::JsonDialog)
{
    ui->setupUi(this);
}

JsonDialog::~JsonDialog()
{
    delete ui;
}
