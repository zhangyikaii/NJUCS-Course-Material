#ifndef USER_H
#define USER_H

#include <QDialog>
#include <QTimer>
#include <QTime>
#include <QtMath>
#include <QPainter>

namespace Ui {
class User;
}

class User : public QDialog
{
    Q_OBJECT

public:
    explicit User(QWidget *parent = 0);
    ~User();

protected:
    QRectF textRectF(double radius, int pointSize, double angle);
    void paintEvent(QPaintEvent *event);
private:
    Ui::User *ui;
};

#endif // USER_H
