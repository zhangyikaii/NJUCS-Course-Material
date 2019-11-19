#include "finddialog.h"
#include "ui_finddialog.h"

FindDialog::FindDialog(QWidget *parent, QString flag) : QDialog(parent), ui(new Ui::FindDialog)
{
    ui->setupUi(this);
    // 设置默认tab
    if(flag == "find")
    {
        ui->tabWidget->setCurrentIndex(0);
    }
    if(flag == "replace")
    {
        ui->tabWidget->setCurrentIndex(1);
    }
}

FindDialog::~FindDialog()
{
    delete ui;
}

void FindDialog::on_findNextOneButton_clicked()
{
    // 查找的字符串
    QString findStr = ui->comboBox->currentText();
    // 设置查找模式
    QTextDocument::FindFlags flag;

    if(ui->findReverseCk->isChecked())
        flag |= QTextDocument::FindBackward;//反向查找 默认前向
    if(ui->matchCaseCk->isChecked())
        flag |= QTextDocument::FindCaseSensitively;//匹配大小写 默认是不敏感的
    if(ui->matchWholeWordCk->isChecked())
        flag |= QTextDocument::FindWholeWords;//全词匹配 默认否
    // 查找
    if(!docmainEdit->find(findStr, flag))
    {
        //QMessageBox::warning(this, tr("Find"), tr("Can't find %1").arg(str));
        // 显示结果在statusLabel上
        ui->statusLabel->setText(tr("Can't find %1").arg(findStr));
    }else{
        ui->statusLabel->setText(tr(""));
    }

    //更新combox
    updateCombox(ui->comboBox);

}

void FindDialog::on_countButton_clicked()
{
    // 查找的字符串
    QString findStr = ui->comboBox->currentText();
    // 设置查找模式
    QTextDocument::FindFlags flag;
    if(ui->findReverseCk->isChecked())
     flag |= QTextDocument::FindBackward;//反向查找 默认前向
    if(ui->matchCaseCk->isChecked())
     flag |= QTextDocument::FindCaseSensitively;//匹配大小写 默认是不敏感的
    if(ui->matchWholeWordCk->isChecked())
     flag |= QTextDocument::FindWholeWords;//全词匹配 默认否

    int counts = 0;
    // 将cursor移至起始位置
    docmainEdit->moveCursor(QTextCursor::Start);
    // 查找所有出现的位置并统计总数
    while(docmainEdit->find(findStr, flag)) counts++;

    //QMessageBox::warning(this, tr("Find"), tr("Count: %1 match").arg(counts));
    // 显示结果在statusLabel上
    ui->statusLabel->setText(tr("Count: %1 match").arg(counts));
    // 重新将cursor移至起始位置
    docmainEdit->moveCursor(QTextCursor::Start);

    //更新combox
    updateCombox(ui->comboBox);

}

void FindDialog::on_showAllMatchesButon_clicked()
{
    // 查找的字符串
    QString findStr = ui->comboBox->currentText();
    // 设置查找模式
    QTextDocument::FindFlags flag;
    if(ui->findReverseCk->isChecked())
     flag |= QTextDocument::FindBackward;//反向查找 默认前向
    if(ui->matchCaseCk->isChecked())
     flag |= QTextDocument::FindCaseSensitively;//匹配大小写 默认是不敏感的
    if(ui->matchWholeWordCk->isChecked())
     flag |= QTextDocument::FindWholeWords;//全词匹配 默认否

    // 将cursor移至起始位置
    docmainEdit->moveCursor(QTextCursor::Start);

    QList<QTextEdit::ExtraSelection> extraSelections;
    // 高亮颜色
    QColor color = QColor(Qt::green).lighter(150);
    // 查找所有出现的位置并高亮
    int counts=0;
    while(docmainEdit->find(findStr, flag))
    {
        QTextEdit::ExtraSelection extra;
        extra.format.setBackground(color);
        extra.cursor = docmainEdit->textCursor();
        extraSelections.append(extra);
        counts++;
    }
    docmainEdit->setExtraSelections(extraSelections);
    // 重新将cursor移至起始位置
    docmainEdit->moveCursor(QTextCursor::Start);
    if(counts==0)
        ui->statusLabel->setText(tr("Can't find %1").arg(findStr));

    //更新combox
    updateCombox(ui->comboBox);

}

void FindDialog::on_cancelButton_clicked()
{
    FindDialog::close();
}

void FindDialog::on_cancelButton_2_clicked()
{
    FindDialog::close();
}

/*更新ComboBox的Item*/
void FindDialog::updateCombox(QComboBox *box)
{
    if(box->findText(box->currentText())==-1)
    {
       box->addItem(box->currentText());//确保唯一性
    }

}

void FindDialog::on_findNextOneButton_2_clicked()
{
    // 查找的字符串
    QString findStr = ui->comboBox_2->currentText();
    // 设置查找模式
    QTextDocument::FindFlags flag;
    if(ui->findReverseCk_2->isChecked())
        flag |= QTextDocument::FindBackward;//反向查找 默认前向
    if(ui->matchCaseCk_2->isChecked())
        flag |= QTextDocument::FindCaseSensitively;//匹配大小写 默认是不敏感的
    if(ui->matchWholeWordCk_2->isChecked())
        flag |= QTextDocument::FindWholeWords;//全词匹配 默认否
    // 查找
    if(!docmainEdit->find(findStr, flag))
    {
        // 显示结果在statusLabel上
        ui->statusLabel->setText(tr("Can't find %1").arg(findStr));
    }else{
        ui->statusLabel->setText(tr(""));
    }

    //更新combox
    updateCombox(ui->comboBox_2);
}

void FindDialog::on_replaceButton_clicked()
{
    // 查找的字符串
    QString findStr = ui->comboBox_2->currentText();
    if(findStr.isEmpty())
    {
        ui->statusLabel->setText(tr("Find target can't be empty"));
        return;
    }

    // 设置查找模式
    QTextDocument::FindFlags flag;
    if(ui->findReverseCk_2->isChecked())
        flag |= QTextDocument::FindBackward;//反向查找 默认前向
    if(ui->matchCaseCk_2->isChecked())
        flag |= QTextDocument::FindCaseSensitively;//匹配大小写 默认是不敏感的
    if(ui->matchWholeWordCk_2->isChecked())
        flag |= QTextDocument::FindWholeWords;//全词匹配 默认否

    // 获取光标对象
    QTextCursor cursor = docmainEdit->textCursor();

    // 替换的字符串
    QString replaceStr = ui->comboBox_3->currentText();
    // 当前选中的字符串是需要替换的 之所以被选中很可能是之前查找的结果
    if(cursor.hasSelection() && cursor.selectedText() == replaceStr)
    {
        cursor.removeSelectedText();
        cursor.insertText(replaceStr);
    }
    else
    {
        // 查找
        if(!docmainEdit->find(findStr, flag))
        {
            // 显示结果在statusLabel上
            ui->statusLabel->setText(tr("Can't find %1").arg(findStr));
        }else{
            ui->statusLabel->setText(tr(""));
        }
        if(cursor.hasSelection())
        {
            cursor.removeSelectedText();
            cursor.insertText(replaceStr);
        }

    }

    //更新combox
    updateCombox(ui->comboBox_2);
    updateCombox(ui->comboBox_3);
}

void FindDialog::on_replaceAllButton_clicked()
{
    // 查找的字符串
    QString findStr = ui->comboBox_2->currentText();
    if(findStr.isEmpty())
    {
        ui->statusLabel->setText(tr("Find target can't be empty"));
        return;
    }

    // 设置查找模式
    QTextDocument::FindFlags flag;
    if(ui->findReverseCk_2->isChecked())
        flag |= QTextDocument::FindBackward;//反向查找 默认前向
    if(ui->matchCaseCk_2->isChecked())
        flag |= QTextDocument::FindCaseSensitively;//匹配大小写 默认是不敏感的
    if(ui->matchWholeWordCk_2->isChecked())
        flag |= QTextDocument::FindWholeWords;//全词匹配 默认否

    // 替换的字符串
    QString replaceStr = ui->comboBox_3->currentText();

    // 将cursor移至起始位置
    docmainEdit->moveCursor(QTextCursor::Start);

    // 获取光标对象
    //QTextCursor cursor = docmainEdit->textCursor();

    // 统计替换的次数
    int counts = 0;
    // 查找所有出现的位置并替换字符串
    while(docmainEdit->find(findStr, flag))
    {
        docmainEdit->textCursor().removeSelectedText();
        docmainEdit->textCursor().insertText(replaceStr);
        counts++;
    }

    // 重新将cursor移至起始位置
    docmainEdit->moveCursor(QTextCursor::Start);

    //显示结果
    if(counts==0)
        ui->statusLabel->setText(tr("Can't find %1").arg(findStr));
    else
        ui->statusLabel->setText(tr("Replace All: %1 occurrences were replaced").arg(counts));

    //更新combox
    updateCombox(ui->comboBox_2);
    updateCombox(ui->comboBox_3);

}


