"""
Задание 2: простое веб-приложение, которое на ЛЮБОЙ GET-запрос
возвращает страницу «Контакты».

Что закрыто по критериям:
  * HTML читается из файла через контекстный менеджер with open();
  * ответ отдаётся с Content-Type: text/html;
  * любой GET -> страница «Контакты»;
  * дополнительно: страницы ошибок 404 и 500;
  * дополнительно (задание со звёздочкой): приём POST-запроса
    и печать в консоль всех данных, которые прислал пользователь.

Запуск (Windows):
    python -m venv venv
    venv\\Scripts\\activate
    pip install -r requirements.txt
    python app.py
Открыть: http://127.0.0.1:5000/
"""

import sys

from flask import Flask, Response, abort, request

app = Flask(__name__)

CONTACTS_FILE = "contacts.html"


# --------------------------------------------------------------------------
# Вспомогательные функции
# --------------------------------------------------------------------------
def read_page(filename):
    """Читает HTML-файл целиком и возвращает его содержимое.

    Именно контекстный менеджер with open(): файл гарантированно
    закрывается после чтения, даже если что-то пойдёт не так.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def safe_print(text=""):
    """print, который не падает на кириллице в консоли Windows."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "backslashreplace").decode("ascii"))


def print_post_data():
    """Дополнительное задание: печатаем в консоль ВСЁ, что прислал пользователь."""
    safe_print("")
    safe_print("=" * 60)
    safe_print("ПОЛУЧЕН POST-ЗАПРОС")
    safe_print("=" * 60)
    safe_print("URL: " + request.url)
    safe_print("Метод: " + request.method)

    safe_print("-- Заголовки --")
    for key, value in request.headers.items():
        safe_print("  {}: {}".format(key, value))

    safe_print("-- Query-параметры (request.args) --")
    safe_print("  " + repr(request.args.to_dict(flat=False)))

    safe_print("-- Данные формы (request.form) --")
    safe_print("  " + repr(request.form.to_dict(flat=False)))

    safe_print("-- Сырое тело запроса --")
    safe_print("  " + repr(request.get_data(as_text=True)))

    safe_print("-- JSON (если был) --")
    safe_print("  " + repr(request.get_json(silent=True)))

    safe_print("=" * 60)
    safe_print("")


# --------------------------------------------------------------------------
# Строгая версия задания 2: ЛЮБОЙ GET -> страница «Контакты»
# --------------------------------------------------------------------------
@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def any_page(path):
    """Ловит вообще любой адрес и отдаёт «Контакты»."""
    if request.method == "POST":
        # Задание со звёздочкой: данные POST печатаются в консоль.
        print_post_data()

    html = read_page(CONTACTS_FILE)

    # mimetype="text/html" -> в ответе будет Content-Type: text/html; charset=utf-8
    return Response(html, mimetype="text/html")


# --------------------------------------------------------------------------
# Дополнительный функционал: страницы ошибок 404 и 500
# --------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    html = read_page("404.html")
    return Response(html, status=404, mimetype="text/html")


@app.errorhandler(500)
def internal_error(error):
    html = read_page("500.html")
    return Response(html, status=500, mimetype="text/html")


# Демонстрационные маршруты, чтобы страницы ошибок можно было показать в PR.
# На работу основного задания не влияют, при желании удалите.
@app.route("/test-404")
def test_404():
    abort(404)


@app.route("/test-500")
def test_500():
    # Специально ломаем обработчик, чтобы увидеть 500
    1 / 0


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)