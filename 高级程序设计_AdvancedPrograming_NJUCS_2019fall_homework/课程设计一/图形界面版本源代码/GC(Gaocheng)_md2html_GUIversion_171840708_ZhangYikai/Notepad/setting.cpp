#include "setting.h"
#include "ui_setting.h"

Setting::Setting(QWidget *parent) : QDialog(parent), ui(new Ui::Setting)
{
    ui->setupUi(this);
    this->setWindowTitle(tr("Options"));
    setting = new QSettings("config.ini", QSettings::IniFormat);//ini文件
    Init();
}

Setting::~Setting()
{
    delete ui;
}


void Setting::Init()
{
    leftList = new QListWidget(this);
    InitList();

    rightStack = new QStackedWidget(this);
    InitStack();

    QHBoxLayout *mainLayout = new QHBoxLayout(this);
    mainLayout->setMargin(5);
    mainLayout->setSpacing(5);
    mainLayout->addWidget(leftList);
    mainLayout->addWidget(rightStack);
    //设置左侧list所占的宽度
    mainLayout->setStretchFactor(leftList, 1);
    mainLayout->setStretchFactor(rightStack, 5);
    connect(leftList, SIGNAL(currentRowChanged(int)), rightStack, SLOT(setCurrentIndex(int)));
}

void Setting::InitList()
{
    leftList->insertItem(0, tr("Environment"));
    leftList->insertItem(1, tr("Editor"));

}

void Setting::InitStack(){
    rightStack->addWidget(new EnvironmentPage(setting, this));
    rightStack->addWidget(new EditorPage(setting, this));

}



//EnvironmentPage
EnvironmentPage::EnvironmentPage(QSettings *settings,QWidget *parent): QWidget(parent)
{
    //ini文件
    setting = settings;

    //主布局 title+tabs
    QGridLayout *mainLayout = new QGridLayout(this);

    //title
    QLabel *title = new QLabel(tr("Environment"));
    title->setFont(QFont("Microsoft Yahei", 12));

    //tabs
    QTabWidget *tabPage = new QTabWidget;

    auto tab1 = SetInterfaceTab();
    auto tab2 = SetSystemTab();

    //tab添加到tabs上
    tabPage->addTab(tab1, tr("Interface"));
    tabPage->addTab(tab2, tr("System"));

    //title+tabs添加到主布局上
    mainLayout->addWidget(title);
    mainLayout->addWidget(tabPage);
}

QWidget *EnvironmentPage::SetInterfaceTab()
{
    QWidget *tab = new QWidget;

    //分组1
    QGroupBox *box = new QGroupBox(tr("User Interface"), tab);
    //分组1主布局
    QVBoxLayout *layout = new QVBoxLayout(box);
    //分组1行内布局
    QHBoxLayout *layou1 = new QHBoxLayout;
    QLabel *label1 = new QLabel(tr("Language"));
    QComboBox *comb1 = new QComboBox;
    comb1->addItem(QString("Chinese"));
    comb1->addItem(QString("English"));
    layou1->addWidget(label1);
    layou1->addWidget(comb1);
    //分组1行内布局
    QHBoxLayout *layou2 = new QHBoxLayout;
    QLabel *label2 = new QLabel(tr("Theme"));
    QComboBox *comb2 = new QComboBox;
    comb2->addItem(QString("Light"));
    comb2->addItem(QString("Dark"));
    layou2->addWidget(label2);
    layou2->addWidget(comb2);
    //分组1行内布局
    QHBoxLayout *layou3 = new QHBoxLayout;
    QLabel *label3 = new QLabel(tr("Color"));
    layou3->addWidget(label3);

    layout->addLayout(layou1);
    layout->addLayout(layou2);
    layout->addLayout(layou3);
    layout->addStretch(1);

    //保存至setting

    //信号
    connect(comb1, QOverload<const QString &>::of(&QComboBox::currentIndexChanged), [=](const QString &text)
    {
        setting->beginGroup("Environment");
        setting->setValue("Language", text);
        setting->endGroup();
    });
    connect(comb2, QOverload<const QString &>::of(&QComboBox::currentIndexChanged), [=](const QString &text)
    {
        setting->beginGroup("Environment");
        setting->setValue("Theme", text);
        setting->endGroup();
    });


    return tab;
}

QWidget *EnvironmentPage::SetSystemTab()
{
    QWidget *tab = new QWidget;

    //分组1
    QGroupBox *box = new QGroupBox(tr("System"), tab);
    //分组1主布局
    QVBoxLayout *layout = new QVBoxLayout(box);
    //组1组件
    QCheckBox *check1 = new QCheckBox(tr("Auto-save modified files"));
    QCheckBox *check2 = new QCheckBox(tr("Minimize the window when close"));
    layout->setSpacing(5);
    layout->addWidget(check1);
    layout->addWidget(check2);
    layout->addStretch(1);

    connect(check1, QOverload<int>::of(&QCheckBox::stateChanged), [=](int state)
    {
        setting->beginGroup("Environment");
        QString value = state==2? "yes":"no";
        setting->setValue("AutoSave", value);
        setting->endGroup();
    });


    connect(check2, QOverload<int>::of(&QCheckBox::stateChanged), [=](int state)
    {
        setting->beginGroup("Environment");
        QString value = state==2? "yes":"no";
        setting->setValue("MinimizeClose", value);
        setting->endGroup();
    });

    return tab;
}


//EditorPage

EditorPage::EditorPage(QSettings *settings, QWidget *parent):QWidget(parent)
{
    //ini文件
    setting = settings;

    //主布局 title+tabs
    QGridLayout *mainLayout = new QGridLayout(this);

    //title
    QLabel *title = new QLabel(tr("Text Editor"));
    title->setFont(QFont("Microsoft Yahei", 12));

    //tabs
    QTabWidget *tabPage = new QTabWidget;

    auto tab1 = SetFontsTab();
    auto tab2 = SetDisplayTab();
    auto tab3 = SetCompletionTab();

    //tab添加到tabs上
    tabPage->addTab(tab1, tr("Fonts"));
    tabPage->addTab(tab2, tr("Display"));
    tabPage->addTab(tab3, tr("Completion"));

    //title+tabs添加到主布局上
    mainLayout->addWidget(title);
    mainLayout->addWidget(tabPage);
}

QWidget *EditorPage::SetFontsTab()
{
    QWidget *tab = new QWidget;

    //分组1
    QGroupBox *box = new QGroupBox(tr("Font"), tab);
    //分组1主布局
    QVBoxLayout *layout = new QVBoxLayout(box);
    //分组1行内布局
    QHBoxLayout *layou1 = new QHBoxLayout;
    QLabel *label1 = new QLabel(tr("Family"));
    QFontComboBox *comb1 = new QFontComboBox;

    layou1->addWidget(label1);
    layou1->addWidget(comb1);
    //分组1行内布局
    QHBoxLayout *layou2 = new QHBoxLayout;
    QLabel *label2 = new QLabel(tr("Size"));
    QComboBox *comb2 = new QComboBox;
    for(int i=6;i<72;i++){
        comb2->addItem(QVariant(i).toString());
    }
    comb2->setCurrentIndex(10);
    layou2->addWidget(label2);
    layou2->addWidget(comb2);
    //分组1行内布局
    QHBoxLayout *layou3 = new QHBoxLayout;
    QLabel *label3 = new QLabel(tr("Zoom"));
    QSpinBox *spin3 = new QSpinBox();
    spin3->setMinimum(10);
    spin3->setMaximum(600);
    spin3->setSingleStep(10);
    spin3->setValue(100);
    spin3->setSuffix("%");

    layou3->addWidget(label3);
    layou3->addWidget(spin3);

    layout->addLayout(layou1);
    layout->addLayout(layou2);
    layout->addLayout(layou3);
    layout->addStretch(1);

    //保存至setting

    //信号
    connect(comb1, QOverload<const QFont &>::of(&QFontComboBox::currentFontChanged), [=](const QFont &font)
    {
        setting->beginGroup("Text Editor");
        setting->setValue("FontFamliy", QVariant(font).toString());
        setting->endGroup();
    });
    connect(comb2, QOverload<const QString &>::of(&QComboBox::currentIndexChanged), [=](const QString &text)
    {
        setting->beginGroup("Text Editor");
        setting->setValue("FontSize", text);
        setting->endGroup();
    });
    connect(spin3, QOverload<const QString &>::of(&QSpinBox::valueChanged), [=](const QString &text)
    {
        setting->beginGroup("Text Editor");
        setting->setValue("FontZoom", text);
        setting->endGroup();
    });

    return tab;
}

QWidget *EditorPage::SetDisplayTab()
{
    QWidget *tab = new QWidget;
    return tab;
}

QWidget *EditorPage::SetCompletionTab()
{
    QWidget *tab = new QWidget;
    return tab;
}
