import base64
import sys
import requests
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5 import QtCore, QtWidgets, QtGui


# GUI configuration
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Book Suggestor")
        MainWindow.resize(816, 585)
        MainWindow.setMinimumSize(QtCore.QSize(816, 585))
        MainWindow.setMaximumSize(QtCore.QSize(816, 585))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 60, 331, 25))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.txt_new_book = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_new_book.setGeometry(QtCore.QRect(30, 30, 331, 25))
        self.txt_new_book.setObjectName("txt_new_book")
        self.btn_add_book = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_book.setGeometry(QtCore.QRect(360, 30, 89, 25))
        self.btn_add_book.setObjectName("btn_add_book")
        self.list_book = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.list_book.setGeometry(QtCore.QRect(30, 80, 171, 431))
        self.list_book.setObjectName("list_book")
        self.list_category = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.list_category.setGeometry(QtCore.QRect(200, 80, 161, 431))
        self.list_category.setObjectName("list_category")
        self.btn_delete_book = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete_book.setGeometry(QtCore.QRect(30, 520, 89, 25))
        self.btn_delete_book.setObjectName("btn_delete_book")
        self.btn_suggest_books = QtWidgets.QPushButton(self.centralwidget)
        self.btn_suggest_books.setGeometry(QtCore.QRect(700, 510, 111, 41))
        self.btn_suggest_books.setObjectName("btn_suggest_books")
        self.list_new_books = QtWidgets.QTextBrowser(self.centralwidget)
        self.list_new_books.setGeometry(QtCore.QRect(400, 60, 411, 451))
        self.list_new_books.setObjectName("list_new_books")
        self.suggest_amount = QtWidgets.QComboBox(self.centralwidget)
        self.suggest_amount.setGeometry(QtCore.QRect(650, 510, 41, 41))
        self.suggest_amount.setObjectName("suggest_amount")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.suggest_amount.addItem("")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 510, 241, 41))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.btn_clear_suggest = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear_suggest.setGeometry(QtCore.QRect(690, 30, 121, 25))
        self.btn_clear_suggest.setObjectName("btn_clear_suggest")
        self.list_category.raise_()
        self.list_book.raise_()
        self.lineEdit.raise_()
        self.txt_new_book.raise_()
        self.btn_add_book.raise_()
        self.btn_delete_book.raise_()
        self.btn_suggest_books.raise_()
        self.list_new_books.raise_()
        self.suggest_amount.raise_()
        self.lineEdit_2.raise_()
        self.btn_clear_suggest.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Book Suggestor", "Book Suggestor"))
        self.lineEdit.setText(_translate("MainWindow", "Your Books                             Category"))
        self.btn_add_book.setText(_translate("MainWindow", "Add Book"))
        self.btn_delete_book.setToolTip(_translate("MainWindow",
                                                   "<html><head/><body><p>First put the cursor on the book you want to delete</p></body></html>"))
        self.btn_delete_book.setText(_translate("MainWindow", "Delete Book"))
        self.btn_suggest_books.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Click to load more books</p></body></html>"))
        self.btn_suggest_books.setText(_translate("MainWindow", "Suggest Books"))
        self.suggest_amount.setItemText(0, _translate("MainWindow", "1"))
        self.suggest_amount.setItemText(1, _translate("MainWindow", "2"))
        self.suggest_amount.setItemText(2, _translate("MainWindow", "3"))
        self.suggest_amount.setItemText(3, _translate("MainWindow", "4"))
        self.suggest_amount.setItemText(4, _translate("MainWindow", "5"))
        self.suggest_amount.setItemText(5, _translate("MainWindow", "6"))
        self.suggest_amount.setItemText(6, _translate("MainWindow", "7"))
        self.suggest_amount.setItemText(7, _translate("MainWindow", "8"))
        self.suggest_amount.setItemText(8, _translate("MainWindow", "9"))
        self.suggest_amount.setItemText(9, _translate("MainWindow", "10"))
        self.lineEdit_2.setText(_translate("MainWindow", "How Much Books To Suggest ?"))
        self.btn_clear_suggest.setText(_translate("MainWindow", "Clear Suggests"))


# Variable for updating the books
start_index = 0


def get_book_category(book_title) -> str:
    """
    the function use, google api for book and get the book category that is gets from user books
    :param book_title:
    :return: category
    """
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{book_title}",
        "maxResults": 1,
    }

    try:
        # Send an HTTP GET request to the Google Books API
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                book_info = data["items"][0]["volumeInfo"]
                categories = book_info.get("categories", [])
                if categories:
                    return categories.pop()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Book Not Found")
                msg.setText("Sorry can't find book with this name, please recheck again!")
                msg.exec()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Sorry something went wrong, try again!")
            msg.exec()

    except Exception as e:
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(f"error message : {e}")
        msg.exec()


def get_books_by_category(category, amount) -> list:
    """
    the function get all the books that have specific category
    :param amount: amount of book to get
    :param start_index: to add more books each time
    :param category: to search for all books
    :return: list of books
    """
    global start_index
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"subject:{category}",
        "startIndex": start_index,
        "maxResults": {amount},

    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "items" in data:
            books = data["items"]
            return books
        else:
            return []

    except requests.exceptions.RequestException as e:
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(f"error message : {e}")
        msg.exec()


class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_add_book.clicked.connect(self.add_book)
        self.ui.btn_delete_book.clicked.connect(self.delete_book)
        self.ui.btn_suggest_books.clicked.connect(self.suggest_books)
        self.ui.btn_clear_suggest.clicked.connect(lambda: self.ui.list_new_books.clear())
        self.category_list = []
        self.book_list = []
        self.show()

    def add_book(self) -> None:
        """
        the function add book that user insert ,into list
        :return:
        """
        user_book = self.ui.txt_new_book.text()
        if user_book:
            if user_book not in self.book_list:
                category_name = get_book_category(self.ui.txt_new_book.text())
                if category_name:
                    self.category_list.append(category_name)
                    self.ui.list_book.appendPlainText(self.ui.txt_new_book.text())
                    self.book_list.append(self.ui.txt_new_book.text())
                    for item in set(self.category_list):
                        if item not in self.ui.list_category.toPlainText():
                            self.ui.list_category.appendPlainText(item)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Book Exist")
                msg.setText("Book Name Already Exist!")
                msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("No Input")
            msg.setText("Book Name Can't Be Empty")
            msg.exec()

    def delete_book(self) -> None:
        """
        the function delete the book that user want with its category
        :return:
        """
        cursor = self.ui.list_book.textCursor()
        row_number = cursor.blockNumber()
        books = self.ui.list_book.toPlainText().splitlines()
        categories = self.ui.list_category.toPlainText().splitlines()
        if 0 <= row_number < len(books):
            del books[row_number]
            del categories[row_number]
            self.ui.list_book.clear()
            self.ui.list_category.clear()
            for book in books:
                self.ui.list_book.appendPlainText(book)
            for category in categories:
                self.ui.list_category.appendPlainText(category)
            self.book_list = books
            self.category_list = categories

    def suggest_books(self):
        """
        the function suggest books that have the same category as the books the user insert
        :return:
        """
        suggestions = []
        global start_index
        suggest_amount = int(self.ui.suggest_amount.currentText())
        for category in self.category_list:
            category_suggestions = get_books_by_category(category, suggest_amount)
            if not category_suggestions:
                self.ui.list_new_books.insertPlainText(f"No books found for category: {category}")
                self.ui.list_new_books.insertPlainText("\n-------------\n")

            else:
                suggestions.extend(category_suggestions)
        # Get all the book information (image,title,description ... )
        start_index = start_index + suggest_amount
        for book in suggestions:
            preview = f"<a href='{book['volumeInfo']['previewLink']}'>Book Preview</a><br><br>"
            order_book = f"<a href='https://www.google.com/search?q={book['volumeInfo']['title']} order'>Order Book</a><br><br>"
            image_links = book.get('volumeInfo', {}).get('imageLinks', {})
            content_page_link = (image_links.get('smallThumbnail'))
            if content_page_link:
                link = requests.get(content_page_link)
                image_base64 = base64.b64encode(link.content).decode('utf-8')
                img_tag = f'<img src="data:image/jpeg;base64,{image_base64}" alt="Book Cover">'
                self.ui.list_new_books.insertPlainText("")
                self.ui.list_new_books.insertHtml(f"{img_tag}<br>")
            self.ui.list_new_books.insertHtml(f"<b>Title:</b> {book['volumeInfo']['title']}<br>")
            self.ui.list_new_books.insertHtml(f"<b>Category:</b> {', '.join(book['volumeInfo']['categories'])}<br>")
            self.ui.list_new_books.insertHtml(f"<b>Authors: </b>{', '.join(book['volumeInfo']['authors'])}<br>")
            self.ui.list_new_books.insertHtml(f"<b>Description:</b> {book['volumeInfo'].get('description', 'N/A')}<br>")
            self.ui.list_new_books.insertPlainText("\n")
            self.ui.list_new_books.insertHtml(preview)
            self.ui.list_new_books.insertHtml(order_book)
            self.ui.list_new_books.setOpenExternalLinks(True)
            self.ui.list_new_books.insertPlainText("\n-------------\n")


def main():
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
