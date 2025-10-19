#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#include <QtNetwork/QNetworkRequest>
#include <QUrl>
#include <QJsonObject>
#include <QJsonDocument>
#include <QMessageBox>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

//added by Tom
    manager = new QNetworkAccessManager(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

//added by Tom
void MainWindow::on_Embed_clicked()
{
    QString dirPath = ui->dir_path->text().trimmed();
    if (dirPath.isEmpty()) {
        QMessageBox::warning(this, "Missing Path", "Please enter a directory path.");
        return;
    }

    QUrl url("http://127.0.0.1:8000/embed");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject json;
    json["dir_path"] = dirPath;

    QNetworkReply *reply = manager->post(request, QJsonDocument(json).toJson());

    connect(reply, &QNetworkReply::finished, this, [=]() {
        if (reply->error() != QNetworkReply::NoError) {
            QMessageBox::critical(this, "Error", reply->errorString());
        } else {
            QByteArray response_data = reply->readAll();
            QJsonDocument jsonResponse = QJsonDocument::fromJson(response_data);
            QJsonObject obj = jsonResponse.object();

            QString status = obj["status"].toString();
            QString message = obj["message"].toString();

            if (status == "success")
                QMessageBox::information(this, "Success", message);
            else
                QMessageBox::warning(this, "Warning", message);
        }
        reply->deleteLater();
    });
}


// Added by Tom
void MainWindow::on_Query_clicked()
{
    QString question = ui->question->text().trimmed();
    if (question.isEmpty()) {
        QMessageBox::warning(this, "Missing Question", "Please enter a question.");
        return;
    }

    QUrl url("http://127.0.0.1:8000/query");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject json;
    json["question"] = question;
    json["session_id"] = currentSessionId.isEmpty() ? "default" : currentSessionId;


    // disable button while waiting
    ui->Query->setEnabled(false);
    ui->Query->setText("Asking...");

    QNetworkReply *reply = manager->post(request, QJsonDocument(json).toJson());

    connect(reply, &QNetworkReply::finished, this, [=]() {
        ui->Query->setEnabled(true);
        ui->Query->setText("Query");

        if (reply->error() != QNetworkReply::NoError) {
            QMessageBox::critical(this, "Network Error", reply->errorString());
        } else {
            QByteArray responseData = reply->readAll();
            QJsonParseError parseError;
            QJsonDocument doc = QJsonDocument::fromJson(responseData, &parseError);

            if (parseError.error != QJsonParseError::NoError) {
                QMessageBox::critical(this, "Parse Error", parseError.errorString());
            } else {
                QJsonObject obj = doc.object();
                QString answer = obj.value("answer").toString();
                QString context = obj.value("context").toString();

                if (answer.isEmpty()) {
                    QString errorMsg = obj.value("error").toString("No answer received.");
                    QMessageBox::warning(this, "RAG Error", errorMsg);
                } else {
                    ui->Answer->setText(answer);
                    ui->Sources->setText(context);
                }
            }
        }
        reply->deleteLater();
    });
}


void MainWindow::on_SessionID_clicked()
{
    QString sessionid = ui->SessionName->text().trimmed();
    if (sessionid.isEmpty()) {
        QMessageBox::warning(this, "Missing Session ID", "Please enter a session name.");
        return;
    }

    currentSessionId = sessionid;
    QMessageBox::information(this, "Session Set",
                             "Session ID set to: " + currentSessionId);
}

