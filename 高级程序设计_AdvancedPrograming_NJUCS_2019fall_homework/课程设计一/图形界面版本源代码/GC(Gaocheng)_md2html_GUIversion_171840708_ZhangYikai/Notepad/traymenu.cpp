#include "traymenu.h"
#include "traymenu.h"

TrayMenu::TrayMenu(QWidget *parent):QMenu(parent)
{
    createActions();
    createTrayIcon();

    minimizeAction->setEnabled(!isMinimized());
    maximizeAction->setEnabled(!isMaximized());
    restoreAction->setEnabled(isMinimized() || !isMaximized());

    //信号槽连接
    //connect(trayIcon, SIGNAL(messageClicked()), this, SLOT(messageClicked()));
    //connect(trayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), this, SLOT(iconActivated(QSystemTrayIcon::ActivationReason)));

    connect(trayIcon, &QSystemTrayIcon::messageClicked, this, &TrayMenu::messageClicked);
    connect(trayIcon, &QSystemTrayIcon::activated, this, &TrayMenu::iconActivated);
}


void TrayMenu::createActions()
{
    minimizeAction = new QAction(tr("Mi&nimize"), this);
    connect(minimizeAction, &QAction::triggered, this->parentWidget(), &QWidget::hide);

    maximizeAction = new QAction(tr("Ma&ximize"), this);
    connect(maximizeAction, &QAction::triggered, this->parentWidget(), &QWidget::showMaximized);

    restoreAction = new QAction(tr("&Restore"), this);
    connect(restoreAction, &QAction::triggered, this->parentWidget(), &QWidget::showNormal);

    quitAction = new QAction(tr("&Quit"), this);
    connect(quitAction, &QAction::triggered, this->parent(), &QCoreApplication::quit);
}

void TrayMenu::createTrayIcon()
{
    trayIconMenu = new QMenu((QWidget *)this->parent());
    trayIconMenu->addAction(minimizeAction);
    trayIconMenu->addAction(maximizeAction);
    trayIconMenu->addAction(restoreAction);
    trayIconMenu->addSeparator();
    trayIconMenu->addAction(quitAction);

    trayIcon = new QSystemTrayIcon((QWidget *)this->parent());
    trayIcon->setContextMenu(trayIconMenu);
    trayIcon->setIcon(QIcon(":/images/favicon.ico"));
}


void TrayMenu::iconActivated(QSystemTrayIcon::ActivationReason reason)
{
    switch (reason) {
        case QSystemTrayIcon::Trigger:
            this->parentWidget()->showNormal();
        case QSystemTrayIcon::DoubleClick:
            this->parentWidget()->showNormal();
            break;
        case QSystemTrayIcon::MiddleClick:
            showMessage();
            break;
        default:
            ;
    }
}

void TrayMenu::showMessage()
{
    QSystemTrayIcon::MessageIcon msgIcon = QSystemTrayIcon::MessageIcon(QSystemTrayIcon::Information);

    trayIcon->showMessage(tr("Cannot connect to network"),tr("Don't believe me. Honestly, I don't have a "
                                                             "clue.\nClick this balloon for details."), msgIcon, 5000);

}

void TrayMenu::messageClicked()
{
    QMessageBox::information(0, tr("Notepad"),
                             tr("Sorry, I already gave what help I could.\n"
                                "Maybe you should try asking a human?"));
}



