# MyBigNote

The very simple app that draws one note that is currently down on the MIDI-keyboard. It was designed for my good friend Nadya Skvortsova to help her in her musical therapy work.

Очень простое приложение, которое отрисовывает одну нотку, которая сейчас нажата на MIDI-клавиатуре. Я его собрал для моей хорошей подруги — Нади Скворцовой, чтобы помочь ей в её музыкально-терапевтической работе.

![screenshot](screenshot.png)

## Instruction

- Choose midi back-end in the top left corner
- Choose midi device in the top right corner
- If you want to specify the clef — choose it in the bottom left corner

## Инструкция

- Выбрать миди драйвер в левом верхнем углу
- Выбрать миди-устройство (клавиатуру) в верхнем правом углу
- Если нужно использовать конкретный ключ — выбрать его в левом нижнем углу

## Установка

![download](screenshot_download_zip.png)

Скачать всё и распаковать куда-нибудь

### Вариант «если повезёт»

в папке `dist/windows/my_big_note` лежит файл `my_big_note.exe`. Если повезёт — он запустится и всё будет работать.

### Вариант «если не повезло»

Какчаем [это](https://www.python.org/ftp/python/3.9.2/python-3.9.2.exe) и устанавливаем.

**обязательно ставим галочку на «add Python to PATH»**

Потом ищем в меню «Пуск» программу cmd.exe (командная строка)

пишем в ней:

```
pip install -e "путь\к\распакованной\программе\MyBigNote"
```

И потом она должна запускаться также из командной строки, либо: `my_big_note`, либо, если не сработает — `python "путь\к\распакованной\программе\MyBigNote\my_big_note.py"`

К сожалению, ничего приличне по установке не получается...
