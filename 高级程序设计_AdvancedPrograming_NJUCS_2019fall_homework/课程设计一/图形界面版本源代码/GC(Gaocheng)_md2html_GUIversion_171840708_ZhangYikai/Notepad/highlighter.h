#ifndef HIGHLIGHTER_H
#define HIGHLIGHTER_H

#include <QSyntaxHighlighter>
#include <QTextCharFormat>
#include <QRegularExpression>

class Highlighter : public QSyntaxHighlighter
{
    Q_OBJECT
public:
    Highlighter(QTextDocument *parent = 0);

protected:
    void highlightBlock(const QString &text) override;
private:
    struct HighlightingRule
    {
        QRegularExpression pattern;
        QTextCharFormat format;
    };
    QVector<HighlightingRule> highlightingRules;
    // 注释
    QRegularExpression commentStartExpression;
    QRegularExpression commentEndExpression;

    // 关键字
    QTextCharFormat keywordFormat;
    QTextCharFormat classFormat;
    // 单行注释
    QTextCharFormat singleLineCommentFormat;
    // 多行注释
    QTextCharFormat multiLineCommentFormat;
    // 引用
    QTextCharFormat quotationFormat;
    // 函数
    QTextCharFormat functionFormat;


};

#endif // HIGHLIGHTER_H
