#ifndef TRAYMENU_H
#define TRAYMENU_H

#include <QObject>
#include <QWidget>
#include <QMenu>
#include <QSystemTrayIcon>
#include <QCoreApplication>
#include <QDialog>
#include <QMessageBox>
#include <QMainWindow>

class TrayMenu : public QMenu
{
    Q_OBJECT

public:
    explicit TrayMenu(QWidget *parent=0);

    QSystemTrayIcon *trayIcon;
    QMenu *trayIconMenu;

protected:
    void createActions();
    void createTrayIcon();
    void showMessage();
private slots:
    void messageClicked();
    void iconActivated(QSystemTrayIcon::ActivationReason reason);
private:


    QAction *minimizeAction;
    QAction *maximizeAction;
    QAction *restoreAction;
    QAction *quitAction;



};

#endif // TRAYMENU_H
