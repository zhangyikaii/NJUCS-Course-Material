#include "highlighter.h"

Highlighter::Highlighter(QTextDocument *parent): QSyntaxHighlighter(parent)
{
    HighlightingRule rule;

    /***关键词***/
    keywordFormat.setForeground(Qt::darkBlue);
    keywordFormat.setFontWeight(QFont::Bold);
    //设置正则匹配模式 最好写入文件
    QStringList keywordPatterns;
    //数据类型
    keywordPatterns << "\\bchar\\b" << "\\bdouble\\b" << "\\blong\\b"
                    << "\\bint\\b"  << "\\bshort\\b"  << "\\bbool\\b"
                    << "\\bfloat\\b" << "\\benum\\b";
    //修饰符
    keywordPatterns << "\\bsigned\\b" << "\\bunsigned\\b" << "\\bconst\\b"
                    << "\\bprivate\\b" << "\\bprotected\\b" << "\\bpublic\\b"
                    << "\\bstatic\\b" << "\\bstruct\\b" "\\bclass\\b"
                    << "\\bexplicit\\b" << "\\bfriend\\b" << "\\binline\\b"
                    << "\\bnamespace\\b" << "\\boperator\\b" << "\\btemplate\\b"
                    << "\\btypedef\\b" << "\\btypename\\b" << "\\bunion\\b"
                    << "\\bvirtual\\b" << "\\bvoid\\b" << "\\bvolatile\\b" ;

    //运算符
    keywordPatterns << "\\bif\\b" << "\\belse\b" << "\\bswitch\\b"
                    << "\\bdo\\b" <<"\\bwhile\\b" <<"\\bgoto\\b"
                    << "\\bcase\\b" << "\\bcatch\\b" << "\\btry\\b"
                    << "\\bthrow\\b" << "\\binclude\\b";

    foreach (const QString &pattern, keywordPatterns) {
        rule.pattern = QRegularExpression(pattern);
        rule.format = keywordFormat;
        highlightingRules.append(rule);
    }

    /***类名***/
    classFormat.setFontWeight(QFont::Bold);
    classFormat.setForeground(Qt::darkMagenta);
    rule.pattern = QRegularExpression("\\bQ[A-Za-z]+\\b");
    rule.format = classFormat;
    highlightingRules.append(rule);

    /***单行注释***/
    singleLineCommentFormat.setForeground(Qt::red);
    rule.pattern = QRegularExpression("//[^\n]*");
    rule.format = singleLineCommentFormat;
    highlightingRules.append(rule);

    /***多行注释***/
    multiLineCommentFormat.setForeground(Qt::red);

    /***引用***/
    quotationFormat.setForeground(Qt::darkGreen);
    rule.pattern = QRegularExpression("\".*\"");
    rule.format = quotationFormat;
    highlightingRules.append(rule);

    /***函数***/
    functionFormat.setFontItalic(true);
    functionFormat.setForeground(Qt::blue);
    rule.pattern = QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()");
    rule.format = functionFormat;
    highlightingRules.append(rule);

    /***注释***/
    commentStartExpression = QRegularExpression("/\\*");
    commentEndExpression = QRegularExpression("\\*/");

}


void Highlighter::highlightBlock(const QString &text)
{
    foreach (const HighlightingRule &rule, highlightingRules) {
        QRegularExpressionMatchIterator matchIterator = rule.pattern.globalMatch(text);
        while (matchIterator.hasNext()) {
            QRegularExpressionMatch match = matchIterator.next();
            setFormat(match.capturedStart(), match.capturedLength(), rule.format);
        }
    }

    setCurrentBlockState(0);

    int startIndex = 0;
    if (previousBlockState() != 1)
        startIndex = text.indexOf(commentStartExpression);

    while (startIndex >= 0) {

        QRegularExpressionMatch match = commentEndExpression.match(text, startIndex);
        int endIndex = match.capturedStart();
        int commentLength = 0;
        if (endIndex == -1) {
            setCurrentBlockState(1);
            commentLength = text.length() - startIndex;
        } else {
            commentLength = endIndex - startIndex + match.capturedLength();
        }
        setFormat(startIndex, commentLength, multiLineCommentFormat);
        startIndex = text.indexOf(commentStartExpression, startIndex + commentLength);
    }

}
