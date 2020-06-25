#include "MdFile.h"

void MdFile::CreateMdFile(string cont, string fName) {
	if (cont.empty()) {
		string tmp, mdfFile;
		bool flag = false;

		int modee = 0;
		cout << "Please select a mode: (0: Input from CONSOLE; 1: Input from an existing file) :";
		cin >> modee;
		if (modee == 0) {
			do {
				flag = false;
				cout << "Please enter the filename (WITHOUT suffix!): ";
				cin >> fileName;
				getchar();

				mdfFile = fileName + ".md";

				if ((fp = fopen(mdfFile.c_str(), "w")) == NULL) {
					printf("Can't open file(%s)\n", mdfFile.c_str());
					flag = true;
				}
			} while (flag != false);

			// 如果遇到列表, 最大的列表的所有(包含所有子列表)存成一行.
			bool isInList = false;
			string curList;
			while (getline(cin, tmp)) {
				// 第一次遇到list
				if (isInList == false && !tmp.empty() && tmp[0] == '+' || (tmp[0] <= '9' && tmp[0] >= '0' && tmp.size() > 1 && tmp[1] == '.')) {
					isInList = true;
					curList = tmp + "\n";
				}
				// 子list或同级list
				else if (isInList == true && !tmp.empty() && tmp[0] == ' ' || tmp[0] == '+' || (tmp[0] <= '9' && tmp[0] >= '0' && tmp.size() > 1 && tmp[1] == '.')) {
					curList += (tmp + "\n");
				}

				// 即使下一行为空也不能结束.
				//// 结束最大list
				//else if (isInList == true && tmp.empty()) {
				//	vec.push_back(curList);
				//	curList.clear();
				//	isInList = false;
				//}
				// 结束最大list
				else if (isInList == true && !tmp.empty() && (tmp[0] != ' ' || tmp[0] != '+') || (tmp[0] <= '9' && tmp[0] >= '0' && tmp.size() > 1 && tmp[1] == '.')) {
					vec.push_back(curList);
					curList.clear();
					isInList = false;
					vec.push_back(tmp);
				}
				else {
					// 如果下一行为空而且是list构建环境, 就不要放进vec里面.
					if (isInList != true)
						vec.push_back(tmp);
				}
				tmp += "\n";
				fprintf(fp, tmp.c_str());
			}

			if (!curList.empty()) {
				vec.push_back(curList);
			}

			fclose(fp);

		}

		// 从文件读入
		else {
			do {
				flag = false;
				cout << "Please enter the filename (EXISTING file and WITHOUT suffix) :";
				cin >> fileName;
				getchar();

				mdfFile = fileName + ".md";

				if ((fp = fopen(mdfFile.c_str(), "r")) == NULL) {
					printf("Can't open file(%s)\n", mdfFile.c_str());
					flag = true;
				}
			} while (flag != false);

			// 如果遇到列表, 最大的列表的所有(包含所有子列表)存成一行.
			bool isInList = false;
			string curList;
			char buf[100010] = "";
			while (fgets(buf, 100010, fp) != NULL) {
				string tempStr(buf);
				if (tempStr.find("\n") != string::npos)
					tempStr = tempStr.substr(0, tempStr.size() - 1);
				// cout << "--------------------\n" << tempStr << endl;
				// 第一次遇到list
				if (isInList == false && !tempStr.empty() && tempStr[0] == '+' || (tempStr[0] <= '9' && tempStr[0] >= '0' && tempStr.size() > 1 && tempStr[1] == '.')) {
					isInList = true;
					curList = tempStr + "\n";
				}
				// 子list或同级list
				else if (isInList == true && !tempStr.empty() && tempStr[0] == ' ' || tempStr[0] == '+' || (tempStr[0] <= '9' && tempStr[0] >= '0' && tempStr.size() > 1 && tempStr[1] == '.')) {
					curList += (tempStr + "\n");
				}
				// 结束最大list
				else if (isInList == true && !tempStr.empty() && (tempStr[0] != ' ' || tempStr[0] != '+') || (tempStr[0] <= '9' && tempStr[0] >= '0' && tempStr.size() > 1 && tempStr[1] == '.')) {
					vec.push_back(curList);
					curList.clear();
					isInList = false;
					vec.push_back(tempStr);
				}
				else {
					// 如果下一行为空而且是list构建环境, 就不要放进vec里面.
					if (isInList != true)
						vec.push_back(tempStr);
				}
				tempStr += "\n";
				// fprintf(fp, tempStr.c_str());
			}

			if (!curList.empty()) {
				vec.push_back(curList);
			}

			fclose(fp);
		}
	}
	else {
		fileName = fName;
		int dotPos = fileName.find(".md") == string::npos ? fileName.find(".html") : fileName.find(".md");
		if (dotPos != string::npos) {
			fileName = fileName.substr(0, dotPos);
		}

		bool isInList = false;
		string curList, tmp;
		vector<string> tmpVec;
		
		int pos = cont.find('\n');
		int subStart = 0;
		while (string::npos != pos) {

			tmpVec.push_back(cont.substr(subStart, pos - subStart));
			subStart = pos + 1;
			pos = cont.find('\n', subStart);	
		};
		if (string::npos == pos && subStart != cont.length()) {
			// 截取最后一段数据
			tmpVec.push_back(cont.substr(subStart));
		}

		for (int i = 0; i < tmpVec.size(); ++i) {
			// 第一次遇到list
			tmp = tmpVec[i];
			if (isInList == false && !tmp.empty() && tmp[0] == '+' || (tmp[0] <= '9' && tmp[0] >= '0' && tmp.size() > 1 && tmp[1] == '.')) {
				isInList = true;
				curList = tmp + "\n";
			}
			// 子list或同级list
			else if (isInList == true && !tmp.empty() && tmp[0] == ' ' || tmp[0] == '+' || (tmp[0] <= '9' && tmp[0] >= '0' && tmp.size() > 1 && tmp[1] == '.')) {
				curList += (tmp + "\n");
			}

			// 即使下一行为空也不能结束.
			//// 结束最大list
			//else if (isInList == true && tmp.empty()) {
			//	vec.push_back(curList);
			//	curList.clear();
			//	isInList = false;
			//}
			// 结束最大list
			else if (isInList == true && !tmp.empty() && (tmp[0] != ' ' || tmp[0] != '+') || (tmp[0] <= '9' && tmp[0] >= '0' && tmp.size() > 1 && tmp[1] == '.')) {
				vec.push_back(curList);
				curList.clear();
				isInList = false;
				vec.push_back(tmp);
			}
			else {
				// 如果下一行为空而且是list构建环境, 就不要放进vec里面.
				if (isInList != true)
					vec.push_back(tmp);
			}
			tmp += "\n";
			// fprintf(fp, tmp.c_str());
		}

		if (!curList.empty()) {
			vec.push_back(curList);
		}

		// fclose(fp);
	}
}

