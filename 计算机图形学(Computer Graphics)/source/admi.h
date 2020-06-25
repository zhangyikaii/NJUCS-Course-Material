#ifndef ADMI_H
#define ADMI_H

#include <vector>
#include <iostream>
using namespace std;

#include <QDebug>

class Point {
public:
    Point() { }
    Point(int xtmp, int ytmp) : x(xtmp), y(ytmp) { }
    int x, y;
};

class CurvePoint {
public:
    CurvePoint() { }
    CurvePoint(double xtmp, double ytmp) : x(xtmp), y(ytmp) { }

    double x, y;
};


int Round(const double a);

void rotateUpdate(double thet, int &x, int &y);

class Admi
{
public:
    Admi(int idd, vector<int> colo, vector<int> keyVec, bool isDDAorBeziertmp = true) {
        this->id = idd;
        this->color = colo;
        this->keyPoints = keyVec;
        this->isDDAorBezier = isDDAorBeziertmp;
    }

    void DDA(int xa, int ya, int xb, int yb) {
        int dx = xb - xa, dy = yb - ya;
        int eps = std::abs(dx) > std::abs(dy) ? std::abs(dx) : std::abs(dy);
        double x = xa, y = ya, xIncre = double(dx) / double(eps), yIncre = double(dy) / double(eps);
        for (int i = 0; i <= eps; ++i) {
            this->pushPoint((int)(x+0.5),(int)(y+0.5));
            x += xIncre;
            y += yIncre;
        }
    }


    void Bresenham(int x0, int y0, int x1, int y1) {
        bool steep = false;
        if (std::abs(x0-x1) < std::abs(y0-y1)) {
            std::swap(x0, y0);
            std::swap(x1, y1);
            steep = true;
        }
        if (x0 > x1) {
            std::swap(x0, x1);
            std::swap(y0, y1);
        }
        int dx = x1-x0;
        int dy = y1-y0;
        int derror2 = std::abs(dy)*2;
        int error2 = 0;
        int y = y0;
        for (int x = x0; x <= x1; x++) {
            if (steep) {
                this->pushPoint(y, x);
            } else {
                this->pushPoint(x, y);
            }
            error2 += derror2;
            if (error2 > dx) {
                y += (y1>y0?1:-1);
                error2 -= dx*2;
            }
        }
    }

    virtual void pushPoint(int x, int y) {
        allPoint.push_back(Point(x, y));
    }

    void translatePoints(int dx, int dy) {
        for (int i = 0; i < allPoint.size(); ++i) {
            allPoint[i].x += dx;
            allPoint[i].y += dy;
        }
    }

    void rotateKey(double thet) {
        for (int i = 0; i < keyPoints.size(); i += 2) {
            rotateUpdate(thet, keyPoints[i], keyPoints[i + 1]);
        }
    }

    // 直接用公式算.
    virtual void scaleKey(double s, int x, int y) {
        for (int i = 0; i < keyPoints.size(); i += 2) {
            keyPoints[i] = Round(double(keyPoints[i] - x) * s + x);
            keyPoints[i + 1] = Round(double(keyPoints[i + 1] - y) * s + y);
        }
    }

    virtual void translateKey(int dx, int dy) {
        qDebug() << "virtual function error" << endl;
    }
    virtual void myDraw(vector<int> para) {
        qDebug() << "virtual function error" << endl;
    }

    void clearSelf() {
        allPoint.clear();
        keyPoints.clear();
    }

    int id;
    bool isDDAorBezier;

    vector<int> color;
    vector<Point> allPoint;
    vector<int> keyPoints;
};



class Line : public Admi {
public:
    Line(int idd, vector<int> colo, vector<int> keyVec, bool isDDAorBeziertmp = true) : Admi(idd, colo, keyVec, isDDAorBeziertmp) { }

    void translateKey(int dx, int dy) {
        keyPoints[0] += dx;
        keyPoints[1] += dy;
        keyPoints[2] += dx;
        keyPoints[3] += dy;
    }

    void myDraw(vector<int> para) {
        this->allPoint.clear();
        keyPoints = para;
        if (isDDAorBezier == true) {
            this->DDA(para[0], para[1], para[2], para[3]);
        }
        else
            this->Bresenham(para[0], para[1], para[2], para[3]);
    }
};


class Polygon : public Admi {
public:
    Polygon(int idd, vector<int> colo, vector<int> keyVec, bool isDDAorBeziertmp = true) : Admi(idd, colo, keyVec, isDDAorBeziertmp) { }
    void translateKey(int dx, int dy) {
        for (int i = 0; i < keyPoints.size(); i += 2) {
            keyPoints[i] += dx;
            keyPoints[i + 1] += dy;
        }
    }


    void myDraw(vector<int> para) {
        this->allPoint.clear();
        keyPoints = para;
        for (int i = 2; i < para.size(); i += 2) {
            if (isDDAorBezier == true) {
                this->DDA(para[i - 2], para[i - 1], para[i], para[i + 1]);
            }
            else {
                this->Bresenham(para[i - 2], para[i - 1], para[i], para[i + 1]);
            }
        }
        if (isDDAorBezier == true) {
            this->DDA(para[0], para[1], para[para.size() - 2], para[para.size() - 1]);
        }
        else {
            this->Bresenham(para[0], para[1], para[para.size() - 2], para[para.size() - 1]);
        }
        if (isDDAorBezier == true) {
            this->DDA(para[0], para[1], para[2], para[3]);
        }
        else
            this->Bresenham(para[0], para[1], para[2], para[3]);
    }
};



class MyEllipse : public Admi {
public:
    MyEllipse(int idd, vector<int> colo, vector<int> keyVec, bool isDDAorBeziertmp = true) : Admi(idd, colo, keyVec, isDDAorBeziertmp) { }

    void translateKey(int dx, int dy) {
        keyPoints[0] += dx;
        keyPoints[1] += dy;
    }

    void scaleKey(double s, int x, int y) {
        keyPoints[0] = Round(double(keyPoints[0] - x) * s + x);
        keyPoints[1] = Round(double(keyPoints[1] - y) * s + y);
        keyPoints[2] = Round(double(keyPoints[2]) * s);
        keyPoints[3] = Round(double(keyPoints[3]) * s);
    }


    void ellipsePlotPoints(int xCenter, int yCenter, int x, int y) {
        this->pushPoint(xCenter + x, yCenter + y);
        this->pushPoint(xCenter - x, yCenter + y);
        this->pushPoint(xCenter + x, yCenter - y);
        this->pushPoint(xCenter - x, yCenter - y);
    }

    void myDrawEllipse(int xCenter, int yCenter, int Rx, int Ry) {
        int Rx2 = Rx * Rx;
        int Ry2 = Ry * Ry;
        int twoRx2 = 2 * Rx2;
        int twoRy2 = 2 * Ry2;
        int p;
        int x = 0;
        int y = Ry;
        int px = 0;
        int py = twoRx2 * y;

        ellipsePlotPoints(xCenter, yCenter, x, y);
        /* Region 1 */
        p = Round(Ry2 - (Rx2 * Ry) + (0.25 * Rx2));
        while (px < py) {
            x++;
            px += twoRy2;
            if (p < 0) {
                p += Ry2 + px;
            }
            else {
                y--;
                py -= twoRx2;
                p += Ry2 + px - py;
            }
            ellipsePlotPoints(xCenter, yCenter, x, y);
        }
        /* Region 2 */
        p = Round(Ry2 * (x + 0.5) * (x + 0.5) + Rx2 * (y - 1) * (y - 1) - Rx2 * Ry2);
        while (y > 0) {
            y--;
            py -= twoRx2;
            if (p > 0) {
                p += Rx2 - py;
            }
            else {
                x++;
                px += twoRx2;
                p += Rx2 - py + px;
            }
            ellipsePlotPoints(xCenter, yCenter, x, y);
        }
    }

    void myDraw(vector<int> para) {
        this->allPoint.clear();
        keyPoints = para;
        myDrawEllipse(para[0], para[1], para[2], para[3]);
    }
};


class Curve : public Admi {
public:
    Curve(int idd, vector<int> colo, vector<int> keyVec, bool isDDAorBeziertmp = true) : Admi(idd, colo, keyVec, isDDAorBeziertmp) { }
    void translateKey(int dx, int dy) {
        for (int i = 0; i < keyPoints.size(); i += 2) {
            keyPoints[i] += dx;
            keyPoints[i + 1] += dy;
        }
    }

    CurvePoint Approximate(double t, CurvePoint const & pt1, CurvePoint const & pt2) {
        double x = double(pt1.x) * (1-t) + double(pt2.x) * t;
        double y = double(pt1.y) * (1-t) + double(pt2.y) * t;

        return CurvePoint(x, y);
    }

    void Bezier(vector<Point> const & para) {
        for(double t = 0 ; t < 1 ; t = t + 0.005) {
            vector<CurvePoint> temp1;
            for (int i = 0; i < para.size(); ++i)
                temp1.push_back(CurvePoint(double(para[i].x), double(para[i].y)));

            while(temp1.size() > 1) {
                vector<CurvePoint> temp2;
                for(int i = 0 ; i < temp1.size()-1 ; i++) {
                    CurvePoint pt1 = temp1[i];
                    CurvePoint pt2 = temp1[i+1];

                    temp2.push_back(Approximate(t, pt1, pt2));
                }

                temp1 = temp2;
            }

            this->pushPoint(Round(temp1[0].x), Round(temp1[0].y));     // finally only one point will be left
        }
    }


    // 返回 u_i
    double u_i(const int& i) {
        return (double)i;
    }

    double Biku(const int& i, const int& k, const double& u) {
        if (k == 1) {
            if (i <= u && u < i + 1) {
                return 1;
            }
            return 0;
        }

        return (u - u_i(i)) / (u_i(i + k - 1) - u_i(i)) * Biku(i, k - 1, u)
                + (u_i(i + k) - u) / (u_i(i + k) - u_i(i + 1)) * Biku(i + 1, k - 1, u);
    }

    double pu(double u, const int& p1, const int& p2, const int& p3, const int& p4) {
        double a = -u * u * u + 3 * u * u - 3 * u + 1,
                b = 3 * u * u * u - 6 * u * u + 4,
                c = -3 * u * u * u + 3 * u * u + 3 * u + 1,
                d = u * u * u;

        return (a * p1 + b * p2 + c * p3 + d * p4) / 6;
    }

    void Bspline(vector<Point> const & para) {
//        for (int i = 0; i < para.size(); ++i) {
//            cout << para[i].x << " " << para[i].y << endl;
//            this->pushPoint(para[i].x, para[i].y);
//        }
//        int n = para.size();
//        double curX = 0, curY = 0;
//        for (double u = u_i(4 - 1); u <= u_i(n + 1); u += 0.001) {
//            curX = 0, curY = 0;
//            for (int i = 0; i < n; ++i) {
//                curX += (double)para[i].x * Biku(i, 4, u);
//                curY += (double)para[i].y * Biku(i, 4, u);
//            }
//            this->pushPoint(Round(curX), Round(curY));
//        }
        int n = para.size();
        double curX = 0, curY = 0;
        for (double u = 0; u <= 1; u += 0.001) {
            curX = 0, curY = 0;
            for (int i = 0; i < n - 3; ++i) {
                curX = pu(u, para[i].x, para[i + 1].x, para[i + 2].x, para[i + 3].x);
                curY = pu(u, para[i].y, para[i + 1].y, para[i + 2].y, para[i + 3].y);
                this->pushPoint(Round(curX), Round(curY));
            }
        }
    }


    void myDraw(vector<int> para) {
        this->allPoint.clear();
        vector<Point> paraPoint;
        for (int i = 0; i < para.size(); i += 2) {
            paraPoint.push_back(Point(para[i], para[i + 1]));
        }
        if (isDDAorBezier == true) {
            Bezier(paraPoint);
        }
        else {
            Bspline(paraPoint);
        }
    }

};



#endif // ADMI_H
