#include "mainwindow.h"
#include <QApplication>

#include <QPixmap>
#include <QPainter>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <string>
#include <string.h>
#include <QDebug>
#include "admi.h"

using namespace std;


// TODO 裁剪 Cohen Sutherlan 算法当线在窗口外面的时候有点问题, 打印窗口在画布上看看.

//double B03(double u) {
//    if (0 <= u < 1) {
//        return u * u / 2;
//    }
//    else if (1 <= u < 2) {
//        return u * (2 - u) / 2 + (u - 1) * (3 - u) / 2;
//    }
//    else if (2 <= u < 3) {
//        return (3 - u) * (3 - u) / 2;
//    }
//}

//double B13(double u) {
//    if (1 <= u < 2) {
//        return (u - 1) * (u - 1) / 2;
//    }
//    else if (2 <= u < 3) {
//        return (u - 1) * (3 - u) / 2 + (u - 2) * (4 - u) / 2;
//    }
//    else if (3 <= u < 4) {
//        return (4 - u) * (4 - u) / 2;
//    }
//}

// // TODO
//double B33(double u) {

//}

typedef int OutCode;

const int INSIDE = 0; // 0000
const int LEFT = 1;   // 0001
const int RIGHT = 2;  // 0010
const int BOTTOM = 4; // 0100
const int TOP = 8;    // 1000


// this function gives the maximum
double maxi(double arr[], int n) {
    double m = 0;
    for (int i = 0; i < n; ++i)
        if (m < arr[i])
            m = arr[i];
    return m;
}

// this function gives the minimum
double mini(double arr[], int n) {
    double m = 1;
    for (int i = 0; i < n; ++i)
        if (m > arr[i])
            m = arr[i];
    return m;
}

void liang_barsky_clipper(Admi *curFigure,
                          double xmin, double ymin, double xmax, double ymax) {
    int x1 = curFigure->keyPoints[0],
            y1 = curFigure->keyPoints[1],
            x2 = curFigure->keyPoints[2],
            y2 = curFigure->keyPoints[3];

    // defining variables
    double p1 = -(x2 - x1);
    double p2 = -p1;
    double p3 = -(y2 - y1);
    double p4 = -p3;

    double q1 = x1 - xmin;
    double q2 = xmax - x1;
    double q3 = y1 - ymin;
    double q4 = ymax - y1;

    double posarr[5], negarr[5];
    int posind = 1, negind = 1;
    posarr[0] = 1;
    negarr[0] = 0;

    if ((p1 == 0 && q1 < 0) || (p3 == 0 && q3 < 0)) {
        curFigure->clearSelf();
        return;
    }
    if (p1 != 0) {
        double r1 = q1 / p1;
        double r2 = q2 / p2;
        if (p1 < 0) {
            negarr[negind++] = r1; // for negative p1, add it to negative array
            posarr[posind++] = r2; // and add p2 to positive array
        }
        else {
            negarr[negind++] = r2;
            posarr[posind++] = r1;
        }
    }
    if (p3 != 0) {
        double r3 = q3 / p3;
        double r4 = q4 / p4;
        if (p3 < 0) {
            negarr[negind++] = r3;
            posarr[posind++] = r4;
        }
        else {
            negarr[negind++] = r4;
            posarr[posind++] = r3;
        }
    }

    double xn1, yn1, xn2, yn2;
    double rn1, rn2;
    rn1 = maxi(negarr, negind); // maximum of negative array
    rn2 = mini(posarr, posind); // minimum of positive array

    if (rn1 > rn2) { // reject
        curFigure->clearSelf();
        return;
    }

    xn1 = x1 + p2 * rn1;
    yn1 = y1 + p4 * rn1; // computing new points

    xn2 = x1 + p2 * rn2;
    yn2 = y1 + p4 * rn2;


    vector<int> para = { Round(xn1), Round(yn1), Round(xn2), Round(yn2) };

//    cout << Round(xn1) << " " << Round(yn1) << " " << Round(xn2) << " " << Round(yn2) << endl;

    curFigure->myDraw(para);
}

// Compute the bit code for a point (x, y) using the clip rectangle
// bounded diagonally by (xmin, ymin), and (xmax, ymax)

// ASSUME THAT xmax, xmin, ymax and ymin are global constants.

OutCode ComputeOutCode(int x, int y, int xmin, int ymin, int xmax, int ymax) {
    OutCode code;

    code = INSIDE;          // initialised as being inside of [[clip window]]

    if (x < xmin)           // to the left of clip window
        code |= LEFT;
    else if (x > xmax)      // to the right of clip window
        code |= RIGHT;
    if (y < ymin)           // below the clip window
        code |= BOTTOM;
    else if (y > ymax)      // above the clip window
        code |= TOP;

    return code;
}

// Cohen–Sutherland clipping algorithm clips a line from
// P0 = (x0, y0) to P1 = (x1, y1) against a rectangle with
// diagonal from (xmin, ymin) to (xmax, ymax).
void CohenSutherlandLineClipAndDraw(Admi *curFigure,
                                    int xmin, int ymin, int xmax, int ymax) {
    int x0 = curFigure->keyPoints[0],
            y0 = curFigure->keyPoints[1],
            x1 = curFigure->keyPoints[2],
            y1 = curFigure->keyPoints[3];

    // compute outcodes for P0, P1, and whatever point lies outside the clip rectangle
    OutCode outcode0 = ComputeOutCode(x0, y0, xmin, ymin, xmax, ymax);
    OutCode outcode1 = ComputeOutCode(x1, y1, xmin, ymin, xmax, ymax);
    bool accept = false;

    while (true) {
        if (!(outcode0 | outcode1)) {
            // bitwise OR is 0: both points inside window; trivially accept and exit loop
            accept = true;
            break;
        } else if (outcode0 & outcode1) {
            // bitwise AND is not 0: both points share an outside zone (LEFT, RIGHT, TOP,
            // or BOTTOM), so both must be outside window; exit loop (accept is false)
            break;
        } else {
            // failed both tests, so calculate the line segment to clip
            // from an outside point to an intersection with clip edge
            double x, y;

            // At least one endpoint is outside the clip rectangle; pick it.
            OutCode outcodeOut = outcode0 ? outcode0 : outcode1;

            // Now find the intersection point;
            // use formulas:
            //   slope = (y1 - y0) / (x1 - x0)
            //   x = x0 + (1 / slope) * (ym - y0), where ym is ymin or ymax
            //   y = y0 + slope * (xm - x0), where xm is xmin or xmax
            // No need to worry about divide-by-zero because, in each case, the
            // outcode bit being tested guarantees the denominator is non-zero
            if (outcodeOut & TOP) {           // point is above the clip window
                x = x0 + double(x1 - x0) * double(ymax - y0) / double(y1 - y0);
                y = ymax;
            } else if (outcodeOut & BOTTOM) { // point is below the clip window
                x = x0 + double(x1 - x0) * (ymin - y0) / (y1 - y0);
                y = ymin;
            } else if (outcodeOut & RIGHT) {  // point is to the right of clip window
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0);
                x = xmax;
            } else if (outcodeOut & LEFT) {   // point is to the left of clip window
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0);
                x = xmin;
            }

            // Now we move outside point to intersection point to clip
            // and get ready for next pass.
            if (outcodeOut == outcode0) {
                x0 = x;
                y0 = y;
                outcode0 = ComputeOutCode(x0, y0, xmin, ymin, xmax, ymax);
            } else {
                x1 = x;
                y1 = y;
                outcode1 = ComputeOutCode(x1, y1, xmin, ymin, xmax, ymax);
            }
        }
    }
    if (accept) {
        // Following functions are left for implementation by user based on
        // their platform (OpenGL/graphics.h etc.)
        // DrawRectangle(xmin, ymin, xmax, ymax);
        vector<int> para = {x0, y0, x1, y1};
        curFigure->myDraw(para);
    }
    else {
        curFigure->clearSelf();
    }
}

void drawAllonPixmap(const vector<Admi*>& adm, QPainter *painter) {
    for (int i = 0; i < adm.size(); ++i) {
        painter->setPen(QColor(adm[i]->color[0], adm[i]->color[1], adm[i]->color[2]));
//        cout << adm[i]->color[0] << " "
//                                 << adm[i]->color[1] << " "
//                                 << adm[i]->color[2] << endl;
        for (int k = 0; k < adm[i]->allPoint.size(); ++k) {
            painter->drawPoint(adm[i]->allPoint[k].x, adm[i]->allPoint[k].y);
        }
    }

//    cout << "---------" << endl;
}

vector<int> splitCommand(string com) {
    if (com[com.size() - 1] == '\n')
        com = com.substr(0, com.size() - 1);

    vector<int> res;
    int bef = 0, aft = 0;
    while (bef < com.size()) {
        if ((com[bef] <= '9' && com[bef] >= '0') || com[bef] == '-') {
            if (com.find(' ', bef) == string::npos)
                aft = com.size();
            else
                aft = com.find(' ', bef);

            res.push_back(atoi(com.substr(bef, aft - bef).c_str()));
            if (aft == com.size())
                break;
            bef = com.find(' ', bef) + 1;
            continue;
        }
        ++bef;
    }
//    cout << "---------" << endl;
//    for (int i = 0; i < res.size(); ++i) {
//        cout << res[i] << " ";
//    }
//    cout << endl << "---------" << endl;
    return res;
}

void clearAdmi(vector<Admi *> &adm) {
    for (int i = 0; i < adm.size(); ++i) {
        delete adm[i];
    }
    adm.clear();
}

Admi* findId(vector<Admi*> &adm, int curId) {
    for (int i = 0; i < adm.size(); ++i) {
        if (adm[i]->id == curId)
            return adm[i];
    }

    return NULL;
}

void myTranslate(int dx, int dy, Admi* cur) {
    cur->translatePoints(dx, dy);
    cur->translateKey(dx, dy);
}

void myRotate(int x, int y, int r, Admi *cur) {
    double thet = double(r) * 3.1415926535 / 180.0;
    myTranslate(-x, -y, cur);
    cur->rotateKey(thet);

    // rotateUpdate(thet, x, y);

    // move key point at first.
    myTranslate(x, y, cur);
    // then draw
    cur->myDraw(cur->keyPoints);
}

void myScale(int x, int y, double s, Admi *cur) {
    cur->scaleKey(s, x, y);
    cur->myDraw(cur->keyPoints);
}


int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    string commaDir, saveDir;
    if (argc == 3) {
        commaDir = argv[1];
        saveDir = argv[2];
    }

//    FILE* fpDebug = fopen("DEBUG.txt", "w");
//    fputs(commaDir.c_str(), fpDebug);
//    fputs(saveDir.c_str(), fpDebug);
//    fclose(fpDebug);

    vector<Admi *> adm;
    vector<int> curColor;
    curColor.push_back(0);
    curColor.push_back(0);
    curColor.push_back(0);

    int pixmapX = 0, pixmapY = 0;

    const string resetCanvas_comma = "resetCanvas",
            setColor_comma = "setColor",
            drawLine_comma = "drawLine",
            saveCanvas_comma = "saveCanvas",
            drawPolygon_comma = "drawPolygon",
            drawEllipse_comma = "drawEllipse",
            translate_comma = "translate",
            rotate_comma = "rotate",
            clip_comma = "clip",
            curve_comma = "drawCurve",
            scale_comma = "scale";

    // read file.
    vector<string> comVec;
    // commaDir += "input.txt";
    FILE* fp = NULL;
    fp = fopen(commaDir.c_str(), "r");
    if (fp == NULL) {
        return 0;
    }
    while (!feof(fp)) {
        char buf[1010] = "";
        fgets(buf, 1010, fp);
        string s(buf);
        comVec.push_back(s);
    }
    fclose(fp);

    for (int i = 0; i < comVec.size(); ++i) {
        // resetCanvas_comma
        if (comVec[i].find(resetCanvas_comma) != string::npos) {
            int paraBeg = comVec[i].find(resetCanvas_comma) + resetCanvas_comma.size() + 1;
            vector<int> para = splitCommand(comVec[i].substr(paraBeg,
                                          comVec[i].size() - paraBeg));
            if (para.size() == 2) {
                pixmapX = para[0], pixmapY = para[1];
                clearAdmi(adm);
            }
            else {
                // parameter error
            }
        }

        // setColor_comma
        else if (comVec[i].find(setColor_comma) != string::npos) {
            int paraBeg = comVec[i].find(setColor_comma) + setColor_comma.size() + 1;
            vector<int> para = splitCommand(comVec[i].substr(paraBeg,
                                          comVec[i].size() - paraBeg));
            if (para.size() == 3) {
                curColor[0] = para[0];
                curColor[1] = para[1];
                curColor[2] = para[2];
            }
            else {
                // parameter error
            }
        }

        // drawLine_comma
        else if (comVec[i].find(drawLine_comma) != string::npos) {
            int paraBeg = comVec[i].find(drawLine_comma) + drawLine_comma.size() + 1;
            bool isDDA = comVec[i].find("DDA") == string::npos ? false : true;
            int tmpEnd = isDDA == false ? comVec[i].find("Bresenham") : comVec[i].find("DDA");

            vector<int> para = splitCommand(comVec[i].substr(paraBeg,
                                          tmpEnd - paraBeg));

            if (para.size() == 5) {
                int curId = para[0];
                para.erase(para.begin());   // erase ID
                Admi *cur = findId(adm, curId);
                if (cur == NULL) {
                    cur = new Line(curId, curColor, para, isDDA);
                    adm.push_back(cur);
                }

                // cur 现在和adm[]的指向同一个位置.
                cur->myDraw(para);
            }
            else {
                // parameter error
            }
        }


        // drawPolygon_comma
        else if (comVec[i].find(drawPolygon_comma) != string::npos) {
            int paraBeg = comVec[i].find(drawPolygon_comma) + drawPolygon_comma.size() + 1;
            bool isDDA = comVec[i].find("DDA") == string::npos ? false : true;
            int midA = 0;
            if (isDDA == false) {
                midA = comVec[i].find("Bresenham");
            }
            else {
                midA = comVec[i].find("DDA");
            }

            vector<int> paraM = splitCommand(comVec[i].substr(paraBeg, midA - paraBeg)),
                    paraN = splitCommand(comVec[i + 1]);
            ++i;    // read parameters.


            if (paraM.size() == 2 && paraN.size() == paraM[1] * 2) {
                // new object
                int curId = paraM[0];
                Admi *cur = findId(adm, curId);
                if (cur == NULL) {
                    cur = new Polygon(curId, curColor, paraN, isDDA);
                    adm.push_back(cur);
                }

                // only one Point
                if (paraM[1] == 1) {
                    cur->pushPoint(paraN[0], paraN[1]);
                    continue;
                }
                cur->myDraw(paraN);
            }
            else {
                // parameter error
            }

        }

        // drawEllipse_comma
        else if (comVec[i].find(drawEllipse_comma) != string::npos) {
            int paraBeg = comVec[i].find(drawEllipse_comma) + drawEllipse_comma.size() + 1;

            vector<int> para = splitCommand(comVec[i].substr(paraBeg, comVec[i].size() - paraBeg));

            if (para.size() == 5) {
                int curId = para[0];
                para.erase(para.begin());   // erase ID
                Admi *cur = findId(adm, curId);
                if (cur == NULL) {
                    cur = new MyEllipse(curId, curColor, para);
                    adm.push_back(cur);
                }

                // draw ellipse.
                cur->myDraw(para);
            }
            else {
                // parameter error
            }
        }

        // translate_comma
        else if (comVec[i].find(translate_comma) != string::npos) {
            int paraBeg = comVec[i].find(translate_comma) + translate_comma.size() + 1;

            vector<int> para = splitCommand(comVec[i].substr(paraBeg, comVec[i].size() - paraBeg));

            if (para.size() == 3) {
                int curId = para[0];
                para.erase(para.begin());   // erase ID
                Admi *cur = findId(adm, curId);
                if (cur != NULL) {
                    myTranslate(para[0], para[1], cur);
                }
                else {
                    // parameter error
                }
            }
        }

        // rotate_comma
        else if (comVec[i].find(rotate_comma) != string::npos) {
            int paraBeg = comVec[i].find(rotate_comma) + rotate_comma.size() + 1;

            vector<int> para = splitCommand(comVec[i].substr(paraBeg, comVec[i].size() - paraBeg));

            if (para.size() == 4) {
                int curId = para[0];
                para.erase(para.begin());   // erase ID
                Admi *cur = findId(adm, curId);
                if (cur != NULL) {
                    myRotate(para[0], para[1], para[2], cur);
                }
                else {
                    // parameter error
                }
            }
        }

        // clip_comma
        else if (comVec[i].find(clip_comma) != string::npos) {
            int paraBeg = comVec[i].find(clip_comma) + clip_comma.size() + 1;

            bool isCohen = comVec[i].find("Cohen-Sutherland") == string::npos ? false : true;
            int tmpEnd = isCohen == false ? comVec[i].find("Liang-Barsky") : comVec[i].find("Cohen-Sutherland");

            vector<int> para = splitCommand(comVec[i].substr(paraBeg,
                                          tmpEnd - paraBeg));

            if (para.size() == 5) {
                int curId = para[0];
                para.erase(para.begin());   // erase ID
                Admi *cur = findId(adm, curId);
                if (cur != NULL) {
                    if (isCohen == true) {
                        CohenSutherlandLineClipAndDraw(cur, para[0], para[1], para[2], para[3]);
                    }
                    else {
                        liang_barsky_clipper(cur, para[0], para[1], para[2], para[3]);
                    }
                }
                else {
                    // parameter error
                }
            }
        }


        // curve_comma
        else if (comVec[i].find(curve_comma) != string::npos) {
            int paraBeg = comVec[i].find(curve_comma) + curve_comma.size() + 1;

            bool isBezier = comVec[i].find("Bezier") == string::npos ? false : true;
            int tmpEnd = isBezier == false ? comVec[i].find("B-spline") : comVec[i].find("Bezier");

            vector<int> paraM = splitCommand(comVec[i].substr(paraBeg, tmpEnd - paraBeg)),
                    paraN = splitCommand(comVec[i + 1]);
            ++i;    // read parameters.


            if (paraM.size() == 2 && paraN.size() == paraM[1] * 2) {
                // new object
                int curId = paraM[0];
                Admi *cur = findId(adm, curId);
                if (cur == NULL) {
                    cur = new Curve(curId, curColor, paraN, isBezier);
                    adm.push_back(cur);
                }

                // only one Point
                if (paraM[1] == 1) {
                    cur->pushPoint(paraN[0], paraN[1]);
                    continue;
                }
                cur->myDraw(paraN);
            }
            else {
                // parameter error
            }

        }



        // scale_comma
        else if (comVec[i].find(scale_comma) != string::npos) {
            int paraBeg = comVec[i].find(scale_comma) + scale_comma.size() + 1,
                    mid = comVec[i].find_last_of(' ');

            vector<int> para = splitCommand(comVec[i].substr(paraBeg, mid - paraBeg));
            double scaleMul = atof(comVec[i].substr(mid + 1, comVec.size() - mid - 1).c_str());
            if (para.size() == 3) {
                int curId = para[0];
                para.erase(para.begin());   // erase ID
                Admi *cur = findId(adm, curId);

                if (cur != NULL) {
                    myScale(para[0], para[1], scaleMul, cur);
                }
                else {
                    // parameter error
                }
            }
        }




        // saveCanvas_comma
        else if (comVec[i].find(saveCanvas_comma) != string::npos) {
            int paraBeg = comVec[i].find(saveCanvas_comma) + saveCanvas_comma.size() + 1;
            string para = comVec[i].substr(paraBeg, comVec[i].size());
            if (para[para.size() - 1] == '\n')
                para = para.substr(0, para.size() - 1);
            para = saveDir + para + ".bmp";

            QPixmap *pix = new QPixmap(pixmapX, pixmapY);
            pix->fill(Qt::white);
            QPainter *painter = new QPainter(pix);
            drawAllonPixmap(adm, painter);
            pix->save(QString::fromStdString(para));
            // cout << para << endl;

            delete painter;
            delete pix;
        }
    }

    return 0;
}
