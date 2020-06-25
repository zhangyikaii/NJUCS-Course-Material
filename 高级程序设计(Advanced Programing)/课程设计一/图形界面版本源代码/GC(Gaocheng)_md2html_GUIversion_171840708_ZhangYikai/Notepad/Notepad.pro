#-------------------------------------------------
#
# Project created by QtCreator 2018-02-08T20:57:13
#
#-------------------------------------------------

QT       += core gui network
QT       += printsupport
QT       += charts

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Notepad
TEMPLATE = app
CONFIG+=static

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0


SOURCES += \
        main.cpp \
        notepad.cpp \
    md5dialog.cpp \
    finddialog.cpp \
    highlighter.cpp \
    commonhelper.cpp \
    codeeditor.cpp \
    user.cpp \
    setting.cpp \
    jsondialog.cpp \
    traymenu.cpp \
    statics.cpp \
    Admin.cpp \
    HtmlFile.cpp \
    MdFile.cpp

HEADERS += \
        notepad.h \
    md5dialog.h \
    finddialog.h \
    highlighter.h \
    commonhelper.h \
    codeeditor.h \
    globalmacro.h \
    user.h \
    setting.h \
    jsondialog.h \
    traymenu.h \
    statics.h \
    Admin.h \
    HtmlFile.h \
    MdFile.h

FORMS += \
        notepad.ui \
    md5dialog.ui \
    finddialog.ui \
    user.ui \
    setting.ui \
    jsondialog.ui

RESOURCES += \
    resources.qrc

TRANSLATIONS = NotepadI18N_zh_CN.ts

RC_ICONS += favicon.ico

DISTFILES +=


