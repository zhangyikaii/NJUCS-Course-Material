#pragma once
// #include <bits/stdc++.h>
#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <map>
#include <stdlib.h>
#include <stdio.h>
#include <algorithm>
#include <fcntl.h>
#include <io.h>

using namespace std;

class MdFile
{
public:
	MdFile() : fp(NULL) { }
	void CreateMdFile(string cont, string fName);
	string GetFileName() {
		return fileName;
	}
	vector<string> GetVec() {
		return vec;
	}
private:
	FILE* fp;
	string fileName;
	vector<string> vec;
};

