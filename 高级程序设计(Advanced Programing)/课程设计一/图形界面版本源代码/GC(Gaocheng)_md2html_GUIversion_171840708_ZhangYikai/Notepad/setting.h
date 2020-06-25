#ifndef SETTING_H
#define SETTING_H

#include <QDialog>
#include <QStackedWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QStringListModel>
#include <QLabel>
#include <QListWidget>
#include <QPushButton>
#include <QGroupBox>
#include <QRadioButton>
#include <QCheckBox>
#include <QComboBox>
#include <QSettings>
#include <QFontComboBox>
#include <QSpinBox>

namespace Ui {
class Setting;
}

class Setting : public QDialog
{
    Q_OBJECT

public:
    explicit Setting(QWidget *parent = 0);
    ~Setting();

protected:
    void InitList();
    void Init();
    void InitStack();
    QWidget* CreateEnvironmentPage();
    QWidget* CreateEditorPage();

private:
    Ui::Setting *ui;
    QListWidget *leftList;
    QStackedWidget *rightStack;

    QSettings *setting;

};


class EnvironmentPage : public QWidget
{
    Q_OBJECT
public:
    explicit EnvironmentPage(QSettings *settings, QWidget *parent);
protected:
    QWidget *SetSystemTab();
    QWidget *SetInterfaceTab();
    QSettings *setting;
};

class EditorPage : public QWidget
{
    Q_OBJECT
public:
    explicit EditorPage(QSettings *settings, QWidget *parent);
protected:
    QWidget *SetFontsTab();
    QWidget *SetDisplayTab();
    QWidget *SetCompletionTab();
    QSettings *setting;
};

class CloudPage : public QWidget
{
    Q_OBJECT
public:
    explicit CloudPage(QSettings *settings, QWidget *parent);
protected:
    QSettings *setting;
};




#endif // SETTING_H
