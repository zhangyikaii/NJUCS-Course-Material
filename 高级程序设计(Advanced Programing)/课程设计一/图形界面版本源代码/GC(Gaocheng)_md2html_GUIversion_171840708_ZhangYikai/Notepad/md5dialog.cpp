#include "md5dialog.h"
#include "ui_md5dialog.h"

MD5Dialog::MD5Dialog(QWidget *parent) : QDialog(parent), ui(new Ui::MD5Dialog)
{
    ui->setupUi(this);
    connect(ui->inputTextEdit, SIGNAL(cursorPositionChanged()), this, SLOT(generatemd5() ) );
}

MD5Dialog::~MD5Dialog()
{
    delete ui;
}

void MD5Dialog::on_copyToClipboardButton_clicked()
{
    QString str = ui->outputTextEdit->toPlainText();
    // 获取系统剪贴板指针
    QClipboard *clipboard = QApplication::clipboard();
    // 设置剪贴板内容
    clipboard->setText(str);
}

void MD5Dialog::generatemd5()
{
    // 获取输入
    QString inputStr = ui->inputTextEdit->toPlainText();
    QString output;
    QByteArray bytea, byteb;
    // md5
    QCryptographicHash md(QCryptographicHash::Md5);
    bytea.append(inputStr);
    md.addData(bytea);
    byteb = md.result();
    output.append(byteb.toHex());
    // 输出
    ui->outputTextEdit->document()->setPlainText(output);
}
