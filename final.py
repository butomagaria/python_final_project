import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from collections import Counter

from design import Ui_MainWindow
from user_db_module import UserDB
from movie_db_module import MovieDB
from mood_logic_module import MoodGenreMapper
from ui_events_module import show_message, confirm_action, style_app
from movies_dialog_module import MovieDialog
from genre_chart_dialog import GenreChartDialog


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_db = UserDB()
        self.movie_db = MovieDB()
        self.mood_mapper = MoodGenreMapper()

        self.current_user = None
        self.setup_events()
        self.ui.listWidget.addItems(self.movie_db.get_titles())

    def setup_events(self):
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_2.clicked.connect(self.check_login)
        self.ui.pushButton_3.clicked.connect(self.register_user)
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_11.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_10.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))
        self.ui.pushButton_12.clicked.connect(lambda: show_message("პაროლი", "დაგავიწყდა პაროლი?\nცუდია..."))
        self.ui.pushButton_13.clicked.connect(self.confirm_password)
        self.ui.pushButton_18.clicked.connect(self.handle_profile_edit_exit)
        self.ui.pushButton_15.clicked.connect(self.change_username)
        self.ui.pushButton_16.clicked.connect(self.change_password)
        self.ui.pushButton_17.clicked.connect(self.delete_user)
        self.ui.pushButton_19.clicked.connect(self.change_email)
        self.ui.pushButton_8.clicked.connect(lambda: show_message("დახმარება", "დახმარებისთვის დარეკეთ 112-ში"))
        self.ui.pushButton_7.clicked.connect(lambda: show_message("ჩვენ შესახებ", "პროექტზე მუშაობდნენ:\nმარიამ ბუთიაშვილი\nთეკლა გუმბერიძე\nნუცა გოგიტიძე\nნატალი ქმოსტელი"))
        self.ui.pushButton_5.clicked.connect(self.search_movie)
        self.ui.listWidget.itemClicked.connect(self.display_movie_info)
        self.ui.pushButton_9.clicked.connect(self.suggest_movie_by_mood)
        self.ui.pushButton_14.clicked.connect(self.show_watched_genre_statistics)

    def check_login(self):
        username = self.ui.l.text()
        password = self.ui.lineEdit_2.text()

        for uname, email, passwd in self.user_db.fetch_user_credentials():
            if (username == uname or username == email) and password == passwd:
                self.current_user = uname
                self.ui.label_3.setText(f"{self.current_user}-ს პროფილი")
                self.ui.stackedWidget.setCurrentIndex(2)
                self.refresh_movie_table()
                self.ui.l.clear()
                self.ui.lineEdit_2.clear()
                return

        show_message("შეცდომა", "მომხმარებელი ვერ მოიძებნა ან პაროლი არასწორია")

    def register_user(self):
        uname = self.ui.l_2.text()
        mail = self.ui.lineEdit_4.text()
        passwd1 = self.ui.lineEdit_3.text()
        passwd2 = self.ui.lineEdit_5.text()

        if passwd1 != passwd2:
            show_message("რეგისტრაცია", "შეყვანილი პაროლები არ ემთხვევა ერთმანეთს")
            return

        if self.user_db.user_exists(uname, mail):
            show_message("რეგისტრაცია", "ეს სახელი ან ელფოსტა უკვე არსებობს")
            return
        if len(passwd1) and len(passwd2) < 8:
            show_message('რეგისტრაცია','გთხოვთ შეიყვანოთ პაროლი, რომლის სიგრძე იქნება 8 სიმბოლოზე მეტი')
            return

        self.user_db.add_user(uname, passwd1, mail)
        show_message("რეგისტრაცია", "გილოცავთ, წარმატებით გაიარეთ რეგისტრაცია!")
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.l_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_4.clear()

    def search_movie(self):
        text = self.ui.lineEdit.text().strip().lower()
        filtered = [t for t in self.movie_db.get_titles() if text in t.lower()]
        self.ui.listWidget.clear()
        if filtered:
            self.ui.listWidget.addItems(filtered)
        else:
            show_message("შედეგი არ მოიძებნა", "შეყვანილი სიტყვით ფილმი ვერ მოიძებნა")



    def refresh_movie_table(self):
        self.ui.tableWidget.setRowCount(0)

        watch_later=self.user_db.get_user_movies(self.current_user,"watch_later")
        favorites=self.user_db.get_user_movies(self.current_user,"favorites")
        watched=self.user_db.get_user_movies(self.current_user,"watched")

        max_rows=max(len(watch_later),len(favorites),len(watched))
        for i in range(max_rows):
            self.ui.tableWidget.insertRow(i)
            if i< len(watch_later):
                self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(watch_later[i]))
            if i< len(favorites):
                self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(favorites[i]))
            if i< len(watched):
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(watched[i]))
        self.ui.tableWidget.resizeColumnsToContents()


    def display_movie_info(self,item):
       movie=self.movie_db.get_movie_by_title(item.text())
       if not movie:
            show_message("შეცდომა!","ინფორმაცია ვერ მოძებნა")
            return
       title, year, info, genre = movie
       genre=genre.replace("[","").replace("]","")
       movie_info=f"წელი: {year}\nაღწერა: {info}\nჟანრი: {genre}"

       dialog= MovieDialog(title,movie_info,self)

       if self.current_user:
           if self.user_db.is_movie_in_list(self.current_user,"watch_later",title):
               dialog.watch_later_btn.setIcon(QIcon("icons/clock_full.png.png"))
           else: dialog.watch_later_btn.setIcon(QIcon("icons/clock_empty.png.png"))
           if self.user_db.is_movie_in_list(self.current_user,"favorites",title):
               dialog.fav_btn.setIcon(QIcon("icons/star_full.png.png"))
           else: dialog.fav_btn.setIcon(QIcon("icons/star_empty.png.png"))
           if self.user_db.is_movie_in_list(self.current_user,"watched",title):
               dialog.watched_btn.setIcon(QIcon("icons/check_full.png.png"))
           else: dialog.watched_btn.setIcon(QIcon("icons/check_empty.png.png"))


       dialog.watch_later_btn.clicked.connect(lambda: self.toggle_watch_later(title,dialog.watch_later_btn))
       dialog.fav_btn.clicked.connect(lambda: self.toggle_favorite(title,dialog.fav_btn))
       dialog.watched_btn.clicked.connect(lambda: self.toggle_watched(title,dialog.watched_btn))
       dialog.exec_()


    def toggle_watch_later(self,title,button):
        if not self.current_user:
            show_message("შეცდომა","ავტორიზაცია საჭიროა")
            return
        if self.user_db.is_movie_in_list(self.current_user,"watch_later", title):
            self.user_db.remove_movie_from_list(self.current_user,"watch_later", title)
            button.setIcon(QIcon("icons/clock_empty.png.png"))
        else:
            self.user_db.add_movie_to_list(self.current_user,"watch_later", title)
            button.setIcon(QIcon("icons/clock_full.png.png"))
        self.refresh_movie_table()

    def toggle_favorite(self, title, button):
        if not self.current_user:
            show_message("შეცდომა", "ავტორიზაცია საჭიროა")
            return

        if self.user_db.is_movie_in_list(self.current_user, "favorites", title):
            self.user_db.remove_movie_from_list(self.current_user, "favorites", title)
            button.setIcon(QIcon("icons/star_empty.png.png"))
        else:
            self.user_db.add_movie_to_list(self.current_user, "favorites", title)
            button.setIcon(QIcon("icons/star_full.png.png"))

        self.refresh_movie_table()

    def toggle_watched(self, title, button):
        if not self.current_user:
            show_message("შეცდომა", "ავტორიზაცია საჭიროა")
            return

        if self.user_db.is_movie_in_list(self.current_user, "watched", title):
            self.user_db.remove_movie_from_list(self.current_user, "watched", title)
            button.setIcon(QIcon("icons/check_empty.png.png"))
        else:
            self.user_db.add_movie_to_list(self.current_user, "watched", title)
            button.setIcon(QIcon("icons/check_full.png.png"))

        self.refresh_movie_table()

    def suggest_movie_by_mood(self):
        moods = []
        btns = {
            "funny": self.ui.radioButton,
            "love": self.ui.radioButton_6,
            "sad": self.ui.radioButton_3,
            "bored": self.ui.radioButton_2,
            "surprise": self.ui.radioButton_5,
            "fear": self.ui.radioButton_7,
            "nostalgy": self.ui.radioButton_9,
            "inspiration": self.ui.radioButton_10,
            "psychology": self.ui.radioButton_8,
            "family": self.ui.radioButton_11
        }
        for mood, btn in btns.items():
            if btn.isChecked():
                moods.append(mood)
        if not moods:
            show_message("გაფრთხილება", "გთხოვ, აირჩიე მინიმუმ ერთი განწყობა")
            return

        genres = self.mood_mapper.get_genres_for_moods(moods)
        movie = self.movie_db.get_random_movie_by_genres(genres)

        if movie:
            title, year, info, genre = movie
            genre = genre.replace("[", "").replace("]", "")
            movie_info = f" რეკომენდაცია შენს განწყობაზე:\n\nსათაური: {title}\nწელი: {year}\nაღწერა: {info}\nჟანრი: {genre}"
            dialog=MovieDialog(title,movie_info,self)
            if self.current_user:
                if self.user_db.is_movie_in_list(self.current_user, "watch_later", title):
                    dialog.watch_later_btn.setIcon(QIcon("icons/clock_full.png.png"))
                else: dialog.watch_later_btn.setIcon(QIcon("icons/clock_empty.png.png"))
                if self.user_db.is_movie_in_list(self.current_user, "favorites", title):
                    dialog.fav_btn.setIcon(QIcon("icons/star_full.png.png"))
                else: dialog.fav_btn.setIcon(QIcon("icons/star_empty.png.png"))
                if self.user_db.is_movie_in_list(self.current_user, "watched", title):
                    dialog.watched_btn.setIcon(QIcon("icons/check_full.png.png"))
                else: dialog.watched_btn.setIcon(QIcon("icons/check_empty.png.png"))
            dialog.watch_later_btn.clicked.connect(lambda: self.toggle_watch_later(title,dialog.watch_later_btn))
            dialog.fav_btn.clicked.connect(lambda: self.toggle_favorite(title,dialog.fav_btn))
            dialog.watched_btn.clicked.connect(lambda: self.toggle_watched(title,dialog.watched_btn))
            dialog.exec_()
            return
        else:
            msg = "ასეთი განწყობის ფილმი ვერ მოიძებნა."

            show_message("შენთვის ფილმი", msg)

    def confirm_password(self):
        from PyQt5.QtWidgets import QInputDialog
        if not self.current_user:
            show_message("შეცდომა", "მომხმარებელი არ არის ავტორიზებული")
            return

        text, ok = QInputDialog.getText(self, "დადასტურება", "შეიყვანე პაროლი:", QtWidgets.QLineEdit.Password)
        if ok and text == self.user_db.get_password(self.current_user):
            self.ui.stackedWidget.setCurrentIndex(3)
        else:
            show_message("შეცდომა", "პაროლი არასწორია ან ვერ მოიძებნა")

    def change_username(self):
        new = self.ui.lineEdit_6.text().strip()
        if new == self.current_user:
            self.ui.label_8.setText("იგივე სახელია")
            return
        if not new:
            self.ui.label_8.setText("შიყვანეთ ახალი სახელი")
            return
        if self.user_db.user_exists(new, ""):
            self.ui.label_8.setText("ეს სახელი უკვე არსებობს")
            return
        self.user_db.update_username(self.current_user, new)
        self.current_user = new
        self.ui.label_8.setText("სახელი წარმატებით შეიცვალა")
        self.ui.lineEdit_6.clear()

    def change_password(self):
        new = self.ui.lineEdit_7.text().strip()
        if not new:
            self.ui.label_9.setText("შეიყვანეთ ახალი პაროლი")
            return
        if new == self.user_db.get_password(self.current_user):
            self.ui.label_9.setText("იგივე პაროლია")
            return
        if len(new) < 8:
            show_message('პაროლის შეცვლა','შეიყვანეთ პაროლი,რომლის სიგრძე არის 8 სიმბოლოზე მეტი')
            return
        self.user_db.update_password(self.current_user, new)
        self.ui.label_9.setText("პაროლი შეიცვალა")
        self.ui.lineEdit_7.clear()

    def change_email(self):
        new = self.ui.lineEdit_8.text().strip()
        if not new:
            self.ui.label_7.setText("შეიყვანეთ ელ-ფოსტა")
            return
        if new == self.user_db.get_email(self.current_user):
            self.ui.label_7.setText("იგივე ელფოსტაა")
            return
        self.user_db.update_email(self.current_user, new)
        self.ui.label_7.setText("ელფოსტა შეიცვალა")
        self.ui.lineEdit_8.clear()

    def handle_profile_edit_exit(self):
        username_changed = self.ui.label_8.text() == "სახელი წარმატებით შეიცვალა"
        password_changed = self.ui.label_9.text() == "პაროლი შეიცვალა"
        email_changed = self.ui.label_7.text() == "ელფოსტა შეიცვალა"

        if username_changed or password_changed or email_changed:
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.stackedWidget.setCurrentIndex(2)

    def show_watched_genre_statistics(self):
        if not self.current_user:
            show_message("შეცდომა", "ავტორიზაცია აუცილებელია")
            return

        watched_titles = self.user_db.get_user_movies(self.current_user, "watched")
        if not watched_titles:
            show_message("ინფო", "არ გაქვს მონიშნული ფილმები როგორც ნანახი")
            return

        genres = []
        for title in watched_titles:
            movie = self.movie_db.get_movie_by_title(title)
            if movie:
                genre_str = movie[3]
                genre_list = genre_str.strip("[]").replace("'", "").split(",")
                genres.extend([g.strip() for g in genre_list])

        if not genres:
            show_message("ინფო", "ამ ფილმებს არ აქვთ მითითებული ჟანრი")
            return

        genre_counts = Counter(genres)
        dialog = GenreChartDialog(genre_counts, self)
        dialog.exec_()

    def delete_user(self):
        if confirm_action(self, "გაფრთხილება", f"დარწმუნებული ხარ რომ გსურს {self.current_user} პროფილის წაშლა?") == 16384:
            self.user_db.delete_user(self.current_user)
            show_message("წაშლილია", "თქვენი პროფილი წარმატებით წაიშალა")
            self.ui.stackedWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_app(app)
    win = App()
    win.show()
    sys.exit(app.exec_())