#include "HtmlFile.h"

// bef == '[', aft == ')';
int HtmlFile::Url(int bef, int aft) {
    int mid = vec[ii].find("](", bef);
    if (mid == string::npos) {
        fprintf(fp, "%s", vec[ii].substr(bef, aft + 1 - bef).c_str());
        return TEXT;
    }

    ++bef;
    string urlName = vec[ii].substr(bef, mid - bef), url = vec[ii].substr(mid + 2, aft - mid - 2);

    fprintf(fp, "<a href=\'%s\'>%s</a>", url.c_str(), urlName.c_str());
    return URL;
}

int HtmlFile::DoOneLine(int bef, int aft, bool used[], int befListLevel) {
    if (bef >= aft)
        return TEXT;

    int titl = 0, curLisLevel = 0;
    bool isFront = (bef == 0) ? true : false;

    // 第一次发现QUOTEBLOCK.
    if (isFront == true && used[CODEBLOCK] == false && used[QUOTEBLOCK] == false && LineSize >= 2 && vec[ii][0] == '>' && vec[ii][1] == ' ') {
        used[QUOTEBLOCK] = true;
        fprintf(fp, "<blockquote>");
    }
    else if (used[QUOTEBLOCK] != false && (ii == vec.size() - 1 || (isFront == true  && LineSize >= 2 && vec[ii][0] != '>'))) {
        used[QUOTEBLOCK] = false;
        fprintf(fp, "</blockquote>\n");
    }

    // 列表构建思路:
    // 一个最大的列表预处理成一行(同时根据前面的空格标记层级关系), 用比较好的数据结构存成分层级那样的, 像dfs一样递归搜;
    // 注意大列表中列表小列表中列表 这样的嵌套形式
    while (used[CODEBLOCK] == false && (CurBef == ' ' || CurBef == '>')) {
        if (CurBef == ' ')
            fprintf(fp, " ");
        ++bef;
        ++curLisLevel;
    }

    // 处理分割线和代码块.
    if (isFront == true) {
        if (vec[ii] == "```" && used[CODEBLOCK] == false) {
            used[CODEBLOCK] = true;
            fprintf(fp, "<pre><code>");
            return CODEBLOCK;
        }
        if (used[CODEBLOCK] == true && vec[ii] != "```") {
            fprintf(fp, "%s", vec[ii].c_str());
            return CODEBLOCK;
        }
        else if (used[CODEBLOCK] == true && vec[ii] == "```") {
            fprintf(fp, "</code></pre>\n");
            used[CODEBLOCK] = false;
            return CODEBLOCK;
        }

        int tmpi = 0;
        for (tmpi = 0; tmpi < LineSize; ++tmpi) {
            if (vec[ii][tmpi] != '-' && vec[ii][tmpi] != ' ')
                break;
        }
        if (tmpi == LineSize) {
            fprintf(fp, "<hr />");
            return LINE;
        }
    }

    // 处理单端标记.
    // 标题.
    if (CurBef == '#' && used[TITLE] != true) {
        int tk = bef;
        while (vec[ii][tk] == '#')
            ++tk;
        if (vec[ii][tk] == ' ') {
            titl = tk - bef;
            fprintf(fp, "<h%d>", titl);

            used[TITLE] = true;
            DoOneLine(tk + 1, aft, used);
            used[TITLE] = false;

            fprintf(fp, "</h%i>", titl);
            return TITLE;
        }
    }

    // 列表, 这里是处理已经预处理好的.
    else if (CurBef == '+' || (CurBef <= '9' && CurBef >= '0' && bef < LineSize - 1 && vec[ii][bef + 1] == '.')) {
        bool listType = false;
        char curNum;
        if (CurBef <= '9' && CurBef >= '0') {
            listType = true;
            curNum = CurBef;
        }

        int lisBef = bef + 2, lisAft = vec[ii].find('\n', lisBef), isSonList = 0;	// isSonList : 1(接下来子列表), 2(同级列表), 0(接下来可以结尾了, 当前列表已经结束了).
        if (listType == true)
            lisBef++;

        if (lisAft == string::npos) {
            lisAft = aft;
        }


        bool isPrintul = false;
        if (befListLevel < curLisLevel || (curLisLevel == 0 && used[LIST] == false)) {
            if (listType == true)
                fprintf(fp, "<ol start='' >\n");
            else
                fprintf(fp, "<ul>\n");
            used[LIST] = true;
            isPrintul = true;
        }

        fprintf(fp, "<li>");

        // 先解析本列表项.
        DoOneLine(lisBef, lisAft, used);

        int nexBef = vec[ii].find('+', lisAft);
        for (int ti = lisAft; ti < LineSize; ++ti) {
            if (vec[ii][ti] <= '9' && vec[ii][ti] >= '0' && ti < LineSize - 1 && vec[ii][ti + 1] == '.') {
                if (nexBef > ti || nexBef == string::npos) {
                    nexBef = ti;
                }
                break;
            }
        }
        // 存在接下来的list, 但是不知道级别差异.
        if (nexBef != string::npos) {
            int nexLevel = nexBef - lisAft - 1;
            // 接下来是子list
            if (nexLevel > curLisLevel) {
                isSonList = 1;
            }
            else if (nexLevel == curLisLevel) {
                isSonList = 2;
                fprintf(fp, "</li>\n");
            }
            else {
                fprintf(fp, "</li>\n");
            }
        }
        // 接下来没有了.
        else {
            fprintf(fp, "</li>\n");
        }


        // <li> 是子列表还要包含, 同级不用.
        // <ul> 是子列表和同级都要包含.

        if (isSonList == 1 || isSonList == 2) {
            DoOneLine(lisAft + 1, aft, used, curLisLevel);
            used[LIST] = false;
            if (isSonList == 1)
                fprintf(fp, "</li>\n");
            if (isSonList == 0) {
                if (listType == true)
                    fprintf(fp, "\n</ol>\n");
                else
                    fprintf(fp, "\n</ul>\n");
            }
        }
        else {
            if (isSonList == 0) {
                if (listType == true)
                    fprintf(fp, "\n</ol>\n");
                else
                    fprintf(fp, "\n</ul>\n");
            }
            DoOneLine(lisAft + 1, aft, used, curLisLevel);
            used[LIST] = false;			// 别忘了回溯.
        }


        return LIST;
    }

    else if (used[TEXT] == false && used[TITLE] == false) {
        // raw TEXT
        fprintf(fp, "<p>");
        used[TEXT] = true;
        DoOneLine(bef, aft, used);
        used[TEXT] = false;
        fprintf(fp, "</p>");

        return TEXT;
    }



    ///////////////////////////////////

    // 处理双端标记.
    string& curDo = vec[ii], tmpWrite;
    priority_queue<MyPair> q;
    map<string, int> m;			// 通过hash达到线性时间复杂度.
    m["["] = m["*"] = m["`"] = m["!["] = m["["] = m["**"] = m["***"] = -1;

    // 下面for用于找到最前面(贪心)匹配到的双端标记.
    for (int k = bef; k < aft && k < vec[ii].size(); ++k) {
        char& ch = vec[ii][k];

        // 找双端标记.
        // 解析到双端的首端
        if ((ch == '[' || ch == '!' || ch == '`') && m[StrCh] == -1) {
            m[StrCh] = k;
        }
        else if (ch == '*') {
            int tAft = k;
            while (tAft < LineSize && vec[ii][tAft] == '*') {
                ++tAft;
            }
            string cur = vec[ii].substr(k, tAft - k);
            if (m[cur] == -1)
                m[cur] = k;
            else {
                q.push(MyPair(m[cur], k));
                m[cur] = -1;
            }

            k = tAft - 1;
        }

        // 解析到末端, 而且它的首端已存在.
        else if (ch == ')' && m["["] != -1) {
            q.push(MyPair(m["["], k));
            m["["] = -1;
        }
        else if (ch == '`' && m[StrCh] != -1) {
            q.push(MyPair(m[StrCh], k));
            m[StrCh] = -1;
        }
    }


    // 保证一行内多种环境存在(不管有无嵌套)也可以循环+递归解析.
    while (bef < aft && !q.empty()) {
        MyPair tmp;
        tmp.fir = -1;
        while (!q.empty() && tmp.fir < bef) {
            tmp = q.top();
            q.pop();
        }

        if (tmp.fir < bef)
            break;


        // 现在tmp就是可以处理的双端标记;
        if (tmp.fir > bef) {
            tmpWrite = vec[ii].substr(bef, tmp.fir - bef);
            fprintf(fp, "%s", tmpWrite.c_str());
            bef = tmp.fir;
        }
        if (bef == aft)
            break;

        // 代码
        if (CurBef == '`') {
            fprintf(fp, "<code>");

            used[CODE] = true;
            DoOneLine(tmp.fir + 1, tmp.sec, used);
            used[CODE] = false;

            fprintf(fp, "</code>");
            bef = tmp.sec + 1;
        }
        // 网址
        else if (CurBef == '[') {
            string url, urlName;
            Url(tmp.fir, tmp.sec);
            bef = tmp.sec + 1;
        }

        // 最难处理的粗体斜体嵌套来了.
        else if (CurBef == '*') {
            int cnt = 0, pfir = tmp.fir, psec = tmp.sec;
            while (psec + cnt < aft && vec[ii][pfir + cnt] == '*' && vec[ii][psec + cnt] == '*')
                ++cnt;

            if (cnt >= 3 && used[STRONG] == false && used[ITALIC] == false) {
                fprintf(fp, "<strong><em>");

                // 平行的环境时允许的, 别忘了回溯.
                used[STRONG] = true, used[ITALIC] == true;
                DoOneLine(tmp.fir + 3, tmp.sec, used);
                used[STRONG] = false, used[ITALIC] == false;

                fprintf(fp, "</em></strong>");
                bef = tmp.sec + cnt;
            }
            else if (cnt == 2 && used[STRONG] == false) {
                fprintf(fp, "<strong>");

                used[STRONG] = true;
                DoOneLine(tmp.fir + 2, tmp.sec, used);
                used[STRONG] = false;

                fprintf(fp, "</strong>");
                bef = tmp.sec + cnt;
            }
            else if (cnt == 1 && used[ITALIC] == false) {
                fprintf(fp, "<em>");

                used[ITALIC] = true;
                DoOneLine(tmp.fir + 1, tmp.sec, used);
                used[ITALIC] = false;

                fprintf(fp, "</em>");
                bef = tmp.sec + cnt;
            }
        }

        if (bef != tmp.sec + 1) {
            if (tmp.sec > bef) {
                tmpWrite = vec[ii].substr(bef, tmp.sec - bef);
                fprintf(fp, "%s", tmpWrite.c_str());
                bef = tmp.sec;
            }
        }
    }

    if (bef < aft) {
        tmpWrite = vec[ii].substr(bef, aft - bef);
        fprintf(fp, "%s", tmpWrite.c_str());
        bef = aft;
    }

    return TEXT;
}

void HtmlFile::AddStyle() {
    FILE* cssFp = NULL;
    string cssFileName = CSS_PATH;
    char str[10010] = "";

    fprintf(fp, "%s", "<style>\n");
    if ((cssFp = fopen(cssFileName.c_str(), "r")) == NULL) {
        printf("Can't open file(%s)\n", cssFileName.c_str());
        exit(0);
    }
    else {
        while (!feof(cssFp)) {
            memset(str, 0, sizeof(str));
            fgets(str, sizeof(str - 1), cssFp);

            fprintf(fp, "%s", str);
        }
    }
    fprintf(fp, "%s", "\n</style>\n");
}

void HtmlFile::AddHead() {
    fprintf(fp, "%s", this->styHead1.c_str());
    AddStyle();
    fprintf(fp, "%s%s%s", styHead2.c_str(), fileName.c_str(), styHead3.c_str());
}



void HtmlFile::CreateHtmlFile(MdFile mdfOut) {
    // _setmode(_fileno(fp), _O_U8TEXT);

    int newLinee = 0, quotee = 0, codee = 0, listt = 0, blockk = 0, stat = -1;
    bool used[55] = { 0 };

    this->fileName = mdfOut.GetFileName();

    string hdfName = fileName + ".html";
    this->vec = mdfOut.GetVec();

    fp = fopen(hdfName.c_str(), "w");
    if (fp == NULL) {
        printf("Can't open file(%s)\n", hdfName.c_str());
        exit(0);
    }


    // TODO style 风格选择.
    SetIsStyle(1);
    if (isStyle == 1) {
        AddHead();
    }
    else {
        fprintf(fp, (this->head + fileName + this->subHead).c_str());
    }
    bool isBefEnter = false;
    Fora{
        if (used[CODEBLOCK] != true && vec[ii].empty() && isBefEnter == false) {
            isBefEnter = true;
        }
        else if (used[CODEBLOCK] != true && vec[ii].empty() && isBefEnter == true) {
            fprintf(fp, "<p>&nbsp;</p>\n");
            isBefEnter = false;
        }
        else {
            DoOneLine(0, LineSize, used);
            fprintf(fp, "\n");
            isBefEnter = false;
        }
    }
    fclose(fp);
}
