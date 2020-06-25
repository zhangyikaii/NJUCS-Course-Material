#include "admi.h"


int Round(const double a) { return static_cast<int>(a + 0.5); }

void rotateUpdate(double thet, int &x, int &y) {
    int tmpX = Round((double)x * std::cos(thet) - (double)y * std::sin(thet)),
            tmpY = Round((double)x * std::sin(thet) + (double)y * std::cos(thet));
    x = tmpX;
    y = tmpY;
}
