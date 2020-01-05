#pragma once
#include "common.h"

class linemap {
public:
	linemap() {
		for (int i = 0; i < PER_SOIL_ROW; ++i) {
			l[i].resize(LINE);
		}
	}
	string l[PER_SOIL_ROW];	// 一块地的一行, 纵向6格.
};

