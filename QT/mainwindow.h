#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtNetwork/QNetworkAccessManager>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_Query_clicked();
    void on_Embed_clicked();

private:
    Ui::MainWindow *ui;
// manager added by Tom
    QNetworkAccessManager *manager;
};
#endif // MAINWINDOW_H
