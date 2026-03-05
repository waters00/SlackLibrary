import datetime
from io import BytesIO

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from PIL import Image

from library.models import Reader, Book, Borrowing, custom_path
from library.forms import LoginForm, RegisterForm, ResetPasswordForm, SearchForm


def _create_test_image(name="test.jpg"):
    buf = BytesIO()
    Image.new("RGB", (10, 10), "red").save(buf, "JPEG")
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type="image/jpeg")


def _create_user(username="13800000000", password="testpass123"):
    user = User.objects.create_user(username=username, password=password)
    return user


def _create_reader(user=None, name="测试读者", phone=13800000000):
    if user is None:
        user = _create_user(username=str(phone))
    return Reader.objects.create(user=user, name=name, phone=phone)


def _create_book(isbn="9787000000001", title="测试图书", author="测试作者"):
    return Book.objects.create(
        ISBN=isbn, title=title, author=author, press="测试出版社"
    )


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class CustomPathTest(TestCase):
    def test_generates_unique_filename(self):
        result = custom_path(None, "photo.jpg")
        self.assertTrue(result.endswith(".jpg"))
        self.assertNotEqual(result, "photo.jpg")

    def test_preserves_extension(self):
        self.assertTrue(custom_path(None, "img.png").endswith(".png"))


class ReaderModelTest(TestCase):
    def test_create_reader(self):
        reader = _create_reader()
        self.assertEqual(reader.name, "测试读者")
        self.assertEqual(reader.phone, 13800000000)
        self.assertEqual(reader.max_borrowing, 5)
        self.assertEqual(reader.balance, 0.0)
        self.assertEqual(reader.status, 0)

    def test_str(self):
        reader = _create_reader()
        self.assertEqual(str(reader), "测试读者")

    def test_verbose_name(self):
        self.assertEqual(Reader._meta.verbose_name, "读者")

    def test_one_to_one_user(self):
        user = _create_user()
        reader = _create_reader(user=user)
        self.assertEqual(reader.user, user)
        self.assertEqual(user.reader, reader)


class BookModelTest(TestCase):
    def test_create_book(self):
        book = _create_book()
        self.assertEqual(book.ISBN, "9787000000001")
        self.assertEqual(book.title, "测试图书")
        self.assertEqual(book.quantity, 1)

    def test_str(self):
        book = _create_book()
        self.assertEqual(str(book), "测试图书测试作者")

    def test_verbose_name(self):
        self.assertEqual(Book._meta.verbose_name, "图书")

    def test_default_values(self):
        book = _create_book()
        self.assertEqual(book.category, "文学")
        self.assertEqual(book.location, "图书馆1楼")
        self.assertEqual(book.description, "")


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.reader = _create_reader()
        self.book = _create_book()

    def test_create_borrowing(self):
        today = datetime.date.today()
        b = Borrowing.objects.create(
            reader=self.reader,
            ISBN=self.book,
            date_issued=today,
            date_due_to_returned=today + datetime.timedelta(30),
        )
        self.assertEqual(b.reader, self.reader)
        self.assertEqual(b.ISBN, self.book)
        self.assertIsNone(b.date_returned)
        self.assertEqual(b.amount_of_fine, 0.0)

    def test_str(self):
        today = datetime.date.today()
        b = Borrowing.objects.create(
            reader=self.reader,
            ISBN=self.book,
            date_issued=today,
            date_due_to_returned=today + datetime.timedelta(30),
        )
        self.assertIn("测试读者", str(b))
        self.assertIn("测试图书", str(b))

    def test_verbose_name(self):
        self.assertEqual(Borrowing._meta.verbose_name, "借阅")


# ---------------------------------------------------------------------------
# Form tests
# ---------------------------------------------------------------------------


class LoginFormTest(TestCase):
    def test_valid(self):
        form = LoginForm(data={"username": "user1", "password": "pass1"})
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        form = LoginForm(data={"password": "pass1"})
        self.assertFalse(form.is_valid())

    def test_missing_password(self):
        form = LoginForm(data={"username": "user1"})
        self.assertFalse(form.is_valid())


class RegisterFormTest(TestCase):
    def test_valid_minimal(self):
        form = RegisterForm(data={
            "username": "13800000000",
            "name": "张三",
            "password": "pass123",
            "re_password": "pass123",
        })
        self.assertTrue(form.is_valid())

    def test_email_optional(self):
        form = RegisterForm(data={
            "username": "13800000000",
            "name": "张三",
            "password": "pass123",
            "re_password": "pass123",
        })
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form = RegisterForm(data={
            "username": "13800000000",
            "password": "pass123",
            "re_password": "pass123",
        })
        self.assertFalse(form.is_valid())


class ResetPasswordFormTest(TestCase):
    def test_valid(self):
        form = ResetPasswordForm(data={
            "old_password": "old",
            "new_password": "new",
            "repeat_password": "new",
        })
        self.assertTrue(form.is_valid())

    def test_missing_field(self):
        form = ResetPasswordForm(data={"old_password": "old"})
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    def test_valid(self):
        form = SearchForm(data={"search_by": "书名", "keyword": "Python"})
        self.assertTrue(form.is_valid())

    def test_invalid_choice(self):
        form = SearchForm(data={"search_by": "invalid", "keyword": "Python"})
        self.assertFalse(form.is_valid())

    def test_missing_keyword(self):
        form = SearchForm(data={"search_by": "ISBN"})
        self.assertFalse(form.is_valid())

    def test_default_initial(self):
        form = SearchForm()
        self.assertEqual(form.fields["search_by"].initial, "书名")


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------


class IndexViewTest(TestCase):
    def test_get(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("searchForm", resp.context)
        self.assertTemplateUsed(resp, "library/index.html")


class AboutViewTest(TestCase):
    def test_get(self):
        resp = self.client.get("/about/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "library/about.html")


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = _create_user()

    def test_get(self):
        resp = self.client.get("/login/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "library/login.html")

    def test_authenticated_user_redirected(self):
        self.client.login(username="13800000000", password="testpass123")
        resp = self.client.get("/login/")
        self.assertEqual(resp.status_code, 302)

    def test_login_success(self):
        resp = self.client.post("/login/", {
            "username": "13800000000",
            "password": "testpass123",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, "/")

    def test_login_bad_password(self):
        resp = self.client.post("/login/", {
            "username": "13800000000",
            "password": "wrong",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "not_exist_or_password_error")

    def test_login_nonexistent_user(self):
        resp = self.client.post("/login/", {
            "username": "nobody",
            "password": "wrong",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "not_exist_or_password_error")


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.login(username="13800000000", password="testpass123")

    def test_logout_redirects(self):
        resp = self.client.get("/logout/")
        self.assertEqual(resp.status_code, 302)

    def test_logout_requires_login(self):
        self.client.logout()
        resp = self.client.get("/logout/")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.url)


class RegisterViewTest(TestCase):
    def test_get(self):
        resp = self.client.get("/register/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "library/register.html")

    def test_authenticated_user_redirected(self):
        _create_user()
        self.client.login(username="13800000000", password="testpass123")
        resp = self.client.get("/register/")
        self.assertEqual(resp.status_code, 302)

    def test_register_success(self):
        photo = _create_test_image()
        resp = self.client.post("/register/", {
            "username": "13900000000",
            "name": "新用户",
            "password": "pass123",
            "re_password": "pass123",
            "photo": photo,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "success")
        self.assertTrue(User.objects.filter(username="13900000000").exists())
        self.assertTrue(Reader.objects.filter(name="新用户").exists())

    def test_register_password_mismatch(self):
        resp = self.client.post("/register/", {
            "username": "13900000000",
            "name": "新用户",
            "password": "pass123",
            "re_password": "different",
            "photo": _create_test_image(),
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "repeat_error")

    def test_register_empty_password(self):
        resp = self.client.post("/register/", {
            "username": "13900000000",
            "name": "新用户",
            "password": "",
            "re_password": "",
            "photo": _create_test_image(),
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "empty")

    def test_register_duplicate_user(self):
        _create_user(username="13900000000")
        resp = self.client.post("/register/", {
            "username": "13900000000",
            "name": "新用户",
            "password": "pass123",
            "re_password": "pass123",
            "photo": _create_test_image(),
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "user_exist")


class SetPasswordViewTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.login(username="13800000000", password="testpass123")

    def test_get(self):
        resp = self.client.get("/set_password/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "library/set_password.html")

    def test_change_password_success(self):
        resp = self.client.post("/set_password/", {
            "old_password": "testpass123",
            "new_password": "newpass456",
            "repeat_password": "newpass456",
        })
        self.assertEqual(resp.context["state"], "success")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass456"))

    def test_change_password_mismatch(self):
        resp = self.client.post("/set_password/", {
            "old_password": "testpass123",
            "new_password": "newpass456",
            "repeat_password": "different",
        })
        self.assertEqual(resp.context["state"], "repeat_error")

    def test_change_password_empty_new(self):
        resp = self.client.post("/set_password/", {
            "old_password": "testpass123",
            "new_password": "",
            "repeat_password": "",
        })
        self.assertEqual(resp.context["state"], "empty")

    def test_wrong_old_password(self):
        resp = self.client.post("/set_password/", {
            "old_password": "wrongold",
            "new_password": "newpass456",
            "repeat_password": "newpass456",
        })
        self.assertIsNone(resp.context["state"])

    def test_requires_login(self):
        self.client.logout()
        resp = self.client.get("/set_password/")
        self.assertEqual(resp.status_code, 302)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.reader = _create_reader(user=self.user)

    def test_unauthenticated_redirects(self):
        resp = self.client.get("/profile/")
        self.assertEqual(resp.status_code, 302)

    def test_authenticated(self):
        self.client.login(username="13800000000", password="testpass123")
        resp = self.client.get("/profile/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "library/profile.html")
        self.assertEqual(resp.context["reader"], self.reader)

    def test_no_reader_record(self):
        user2 = _create_user(username="13900000000")
        self.client.login(username="13900000000", password="testpass123")
        resp = self.client.get("/profile/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"no this id reader", resp.content)


class BookSearchViewTest(TestCase):
    def setUp(self):
        _create_book(isbn="9787111111111", title="Python入门", author="张三")
        _create_book(isbn="9787222222222", title="Django实战", author="李四")

    def test_list_all(self):
        resp = self.client.get("/search/", {"keyword": "_书目列表"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["books"].object_list), 2)

    def test_search_by_title(self):
        resp = self.client.get("/search/", {"search_by": "书名", "keyword": "Python"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["books"].object_list), 1)

    def test_search_by_isbn(self):
        resp = self.client.get("/search/", {"search_by": "ISBN", "keyword": "111"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["books"].object_list), 1)

    def test_search_by_author(self):
        resp = self.client.get("/search/", {"search_by": "作者", "keyword": "李四"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["books"].object_list), 1)

    def test_search_no_results(self):
        resp = self.client.get("/search/", {"search_by": "书名", "keyword": "不存在"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["books"].object_list), 0)

    def test_pagination(self):
        for i in range(10):
            _create_book(isbn=f"978700000{i:04d}", title=f"Book{i}", author="A")
        resp = self.client.get("/search/", {"keyword": "_书目列表", "page": "2"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context["books"].object_list) > 0)

    def test_invalid_page(self):
        resp = self.client.get("/search/", {"keyword": "_书目列表", "page": "abc"})
        self.assertEqual(resp.status_code, 200)

    def test_page_out_of_range(self):
        resp = self.client.get("/search/", {"keyword": "_书目列表", "page": "999"})
        self.assertEqual(resp.status_code, 200)


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.book = _create_book()
        self.user = _create_user()
        self.reader = _create_reader(user=self.user)

    def test_get(self):
        resp = self.client.get("/book/detail", {"ISBN": self.book.ISBN})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["book"], self.book)
        self.assertTemplateUsed(resp, "library/book_detail.html")

    def test_no_isbn(self):
        resp = self.client.get("/book/detail")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"no such an ISBN", resp.content)

    def test_invalid_isbn(self):
        resp = self.client.get("/book/detail", {"ISBN": "0000000000000"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"no such an ISBN", resp.content)

    def test_borrow_unauthenticated(self):
        resp = self.client.get(
            "/book/detail", {"ISBN": self.book.ISBN, "action": "borrow"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "no_user")

    def test_borrow_success(self):
        self.client.login(username="13800000000", password="testpass123")
        resp = self.client.get(
            "/book/detail", {"ISBN": self.book.ISBN, "action": "borrow"}
        )
        self.assertEqual(resp.status_code, 302)
        self.reader.refresh_from_db()
        self.assertEqual(self.reader.max_borrowing, 4)
        self.book.refresh_from_db()
        self.assertEqual(self.book.quantity, 0)
        self.assertEqual(Borrowing.objects.count(), 1)

    def test_borrow_upper_limit(self):
        self.client.login(username="13800000000", password="testpass123")
        self.reader.max_borrowing = 0
        self.reader.save()
        resp = self.client.get(
            "/book/detail", {"ISBN": self.book.ISBN, "action": "borrow"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["state"], "upper_limit")


class ReaderOperationViewTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.reader = _create_reader(user=self.user)
        self.book = _create_book()
        self.client.login(username="13800000000", password="testpass123")

    def _create_borrowing(self, days_ago=10, due_days=30):
        issued = datetime.date.today() - datetime.timedelta(days_ago)
        return Borrowing.objects.create(
            reader=self.reader,
            ISBN=self.book,
            date_issued=issued,
            date_due_to_returned=issued + datetime.timedelta(due_days),
        )

    def test_unauthenticated_redirects(self):
        self.client.logout()
        resp = self.client.get("/book/action", {"action": "return_book", "id": 1})
        self.assertEqual(resp.status_code, 302)

    def test_return_book(self):
        b = self._create_borrowing()
        self.reader.max_borrowing = 4
        self.reader.save()
        self.book.quantity = 0
        self.book.save()

        resp = self.client.get("/book/action", {"action": "return_book", "id": b.pk})
        self.assertEqual(resp.status_code, 302)
        b.refresh_from_db()
        self.assertEqual(b.date_returned, datetime.date.today())
        self.reader.refresh_from_db()
        self.assertEqual(self.reader.max_borrowing, 5)
        self.book.refresh_from_db()
        self.assertEqual(self.book.quantity, 1)

    def test_return_overdue_book_has_fine(self):
        issued = datetime.date.today() - datetime.timedelta(40)
        b = Borrowing.objects.create(
            reader=self.reader,
            ISBN=self.book,
            date_issued=issued,
            date_due_to_returned=issued + datetime.timedelta(30),
        )
        self.reader.max_borrowing = 4
        self.reader.save()

        resp = self.client.get("/book/action", {"action": "return_book", "id": b.pk})
        self.assertEqual(resp.status_code, 302)
        b.refresh_from_db()
        self.assertGreater(b.amount_of_fine, 0)

    def test_return_book_no_id(self):
        resp = self.client.get("/book/action", {"action": "return_book"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"no id", resp.content)

    def test_renew_book(self):
        b = self._create_borrowing(days_ago=5, due_days=30)
        original_due = b.date_due_to_returned

        resp = self.client.get("/book/action", {"action": "renew_book", "id": b.pk})
        self.assertEqual(resp.status_code, 302)
        b.refresh_from_db()
        self.assertEqual(b.date_due_to_returned, original_due + datetime.timedelta(30))

    def test_renew_already_extended(self):
        b = self._create_borrowing(days_ago=5, due_days=90)
        original_due = b.date_due_to_returned

        resp = self.client.get("/book/action", {"action": "renew_book", "id": b.pk})
        self.assertEqual(resp.status_code, 302)
        b.refresh_from_db()
        self.assertEqual(b.date_due_to_returned, original_due)

    def test_renew_book_no_id(self):
        resp = self.client.get("/book/action", {"action": "renew_book"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"no id", resp.content)

    def test_unknown_action_redirects(self):
        resp = self.client.get("/book/action", {"action": "unknown"})
        self.assertEqual(resp.status_code, 302)

    def test_no_action_redirects(self):
        resp = self.client.get("/book/action")
        self.assertEqual(resp.status_code, 302)


class StatisticsViewTest(TestCase):
    def test_empty(self):
        resp = self.client.get("/statistics/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "library/statistics.html")

    def test_with_data(self):
        reader = _create_reader()
        book = _create_book()
        today = datetime.date.today()
        Borrowing.objects.create(
            reader=reader,
            ISBN=book,
            date_issued=today,
            date_due_to_returned=today + datetime.timedelta(30),
        )
        resp = self.client.get("/statistics/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("readerData", resp.context)
        self.assertIn("bookData", resp.context)
        self.assertEqual(resp.context["readerData"], ["测试读者"])


# ---------------------------------------------------------------------------
# Management command tests
# ---------------------------------------------------------------------------


class CreateAdminAccountCommandTest(TestCase):
    def test_create_admin(self):
        from django.core.management import call_command
        from io import StringIO

        out = StringIO()
        call_command(
            "create_admin_account",
            username="admin",
            password="admin123",
            stdout=out,
        )
        self.assertIn("成功", out.getvalue())
        user = User.objects.get(username="admin")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("admin123"))

    def test_update_existing_admin(self):
        from django.core.management import call_command
        from io import StringIO

        User.objects.create_superuser("admin", None, "oldpass")
        out = StringIO()
        call_command(
            "create_admin_account",
            username="admin",
            password="newpass",
            stdout=out,
        )
        user = User.objects.get(username="admin")
        self.assertTrue(user.check_password("newpass"))
