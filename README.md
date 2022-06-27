# mgsv-backend

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Stars](https://img.shields.io/github/stars/tinytengu/mgsv-backend?style=flat-square)
![Forks](https://img.shields.io/github/forks/tinytengu/mgsv-backend?style=flat-square)
![Issues](https://img.shields.io/github/issues/tinytengu/mgsv-backend?style=flat-square)

![License](https://img.shields.io/github/license/tinytengu/mgsv-backend?style=flat-square)

RESTful Backend с информацией о прохождении Metal Gear Solid V: Phantom Pain.

Проект содержит интересные твики (миксины, декораторы, ...), поддержку локализации и т.д.

Для проверки кода на соответствие `PEP-8` используется модуль `pycodestyle`, для форматирования модуль `black`, таким образом весь код автоматически форматируется в соответствии со стандартами и рекомендациями при сохранении файла.

# Установка

1. Склонируйте репозиторий
2. Создайте и активируйте виртуальное окружение Python
3. Установите зависимости из `requirements.txt`

```bash
pip install -r requirements.txt
```

4. Проведите миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

---

# Production

Для запуска Production версии проекта необходимо в переменной окружения `DJANGO_SETTINGS_MODULE` прописать путь к файлу `production_settings.py`, а в перменной окружения `SECRET_KEY` секретный ключ для приложения:

Windows (CMD):

```cmd
set DJANGO_SETTINGS_MODULE=mgsv_backend.production_settings
set SECRET_KEY="SOME-SUPER-SECRET-K3Y"
```

Windows (PowerShell):

```powershell
$env:DJANGO_SETTINGS_MODULE="mgsv_backend.production_settings"
$env:SECRET_KEY="SOME-SUPER-SECRET-K3Y"
```

Unix:

```bash
export DJANGO_SETTINGS_MODULE=mgsv_backend.production_settings
export SECRET_KEY="SOME-SUPER-SECRET-K3Y"
```

Но желательно это делать при помощи **Docker**, собирая образы с предустановленными переменными окружения (можно брать из секретных ключей GitHub).

Не забываем с помощью `collectstatic` собирать необходимые статические файлы и хостить их через `nginx`.

Круто бы использовать **CI/CD** на GitHub для процесса валидации, сборки и развертывания всего приложения.

---

# Модели

Основным приложением является `missions`, оно содержит в себе следующие модели и соотвтствующие сериализаторы для DRF:
|Модель|Сериализатор|Описание|
|-|-|-|
|`Character`|`CharacterSerializer`|Персонаж, в основном используется для диалогов
|`Mission`|`MissionSerializer`|Задание (или же Эпизод), имеет внешние связи с `Objective`, `Fact` и `Dialog`.
|`Objective`|`ObjectiveSerializer`|Цель задания, имеет внешние связи с `ObjectiveImage`
|`ObjectiveImage`|`ObjectiveImageSerializer`|Изображение, изображающее цель задания (`Objective`)
|`Fact`|`FactSerializer`|Факт из задания, де-юре и де-факто просто текст с интересной информацией
|`Dialog`|`DialogSerializer`|Диалог, происходящий в задании. Описывает реплики, произносимые различными персонажами в ходе выполнения задания.

Из-за определённой цепочки зависимостей одних сериализаторов от других, в `serializers.py` они записаны в противоположном от Моделей в `models.py` порядке.

---

## Extended сериализаторы

Сериализаторы с постфиксом `Extended` в данном проекте по-сути выступают развёрнутой версией `PrimaryKeyRelatedField`. В то время, как последний отображает только главный ключ `pk` (читайте `id` в 99% случаев), `КакойЛибоСериализаторExtended` отображает развернутую информацию о модели.

Пример:

```python
class ObjectiveSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Objective
        fields = "__all__"

```

<details>
    <summary>Из-за `PrimaryKeyRelatedField` сериализатор будет отображать в `images` лишь поле `id` изображений.</summary>
    <pre>
        <code lang="json">
{
    "id": 5,
    "images": [
        4,
        5,
        6
    ],
    "title": "Эвакуирован пленник, неспособный говорить.",
    "text": "Пленника, неспособного говорить зовут Хамид. ...",
    "type": 1,
    "mission": 1
}
        </code>
    </pre>
</details>

</br>

```python
class ObjectiveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectiveImage
        fields = "__all__"


class ObjectiveSerializerExtended(ObjectiveSerializer):
    images = ObjectiveImageSerializer(many=True, read_only=True)
```

<details>
    <summary>В то время, как `ObjectiveSerializerExtended`, унаследованный от `ObjectiveSerializer` (просто чтобы заново не прописывать класс `Meta`), в качестве поля `images` использует `ObjectiveImageSerializer`, поведение которого возвращает всю информацию об изображении цели, которая и будет выводиться при сериализации.</summary>
    <pre>
        <code lang="json">
{
    "id": 5,
    "images": [
        {
            "id": 4,
            "image": "http://127.0.0.1:8000/media/objectives/Mission_6_punkt_4a.jpg",
            "objective": 5
        },
        {
            "id": 5,
            "image": "http://127.0.0.1:8000/media/objectives/Mission_6_punkt_4b.jpg",
            "objective": 5
        },
        {
            "id": 6,
            "image": "http://127.0.0.1:8000/media/objectives/Mission_6_punkt_4c.jpg",
            "objective": 5
        }
    ],
    "title": "Эвакуирован пленник, неспособный говорить.",
    "text": "Пленника, неспособного говорить зовут Хамид. ...",
    "type": 1,
    "mission": 1
}
        </code>
    </pre>
</details>

---

> Данный подход используется во `ViewSet` для использования параметра `extended=1` в URL. При отсутствии `extended` или `extended=0`, отображается краткая информация о моделях, при `extended=1` и установленном `extended_serializer_class` в нужном `ViewSet`, отображается развернутая информация.

Пример:

```python
# ExtendedViewSetMixin - миксин, отвечающий за работу `extended`, добавляется первым в нужные ViewSet'ы (подробнее см. по ссылке ниже)

class ObjectiveViewSet(ExtendedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ObjectiveSerializer  # Данный сериализатор будет использоваться по умолчанию (без extended или extended=0)
    extended_serializer_class = ObjectiveSerializerExtended  # Данный сериализатор будет использоваться для extended=1
    queryset = Objective.objects.all()
```

Ссылка: [viewsets.py](https://github.com/tinytengu/mgsv-backend/blob/main/mgsv_backend/utils/viewsets.py)

---

## Несколько полей для выборки (MultipleFieldLookupMixin)

По умолчанию DRF позволяет производить выборку во `ViewSet` лишь по одному полю (по умолчанию это `pk`), миксин `MultipleFieldLookupMixin` предзанзачен для расширения данного поведения и позволяет использовать сразу несколько полей в выборке.

Пример:

```python
class MissionViewSet(
    ExtendedViewSetMixin, MultipleFieldLookupMixin, viewsets.ModelViewSet
):
    serializer_class = MissionSerializer
    extended_serializer_class = MissionSerializerExtended
    queryset = Mission.objects.all()
    lookup_fields = ("pk", "slug")
```

Это позволит производить следующий поиск:

- http://127.0.0.1:8000/api/v1/missions/1/ - поиск по `pk`
- http://127.0.0.1:8000/api/v1/missions/0-6-gde-prjachetsja-zhalo/ - поиск по `slug`

Подробнее: [viewsets.py](https://github.com/tinytengu/mgsv-backend/blob/main/mgsv_backend/utils/viewsets.py)

---

## I18N

### Генерация исходников

Проект поддерживает локализацию на различные языки. Обернув необходимый текст в `gettext_lazy` (или `pgettext_lazy` для задания контекста), можно сгенерировать файл для локализации:

1. Переходим в папку с нужным приложением (не рекомендуется это делать в корне всего проекта, иначе захватит локализацию со всех модулей, что будет крайне сложно контролироваьт)

```bash
cd missions
```

2. Собираем все строки и генерируем файл локализации, в данном примере для русского языка

```bash
django-admin makemessages -l ru
```

3. После обнаруживаем в папке `missions` следующую структуру файлов: `locale/ru/LC_MESSAGES/django.po`, в папке `locale` хранятся все локализации, в данном случае дочерняя папка `ru` отвечает за локализацию на русский язык. В файле `django.po` можно обнаружить подобные строки:

```python
#: .\models.py:11
msgid "Subsistence"
msgstr ""

#: .\models.py:12
msgid "Stealth"
msgstr ""
```

В `msgid` указывается текс, обёрнутый ранее в `gettext_lazy` (или иную функцию), это и текст, который будет отображаться при отсутствии перевода и текст, который будет переводиться при наличии перевода в `msgstr`.

Пример:

```python
msgid "Stealth"
msgstr "Скрытно"
```

Все вхождения `gettext_lazy("Stealth")` в данном приложении будут заменены на `Скрытно` при активации русской локали в проекте или у пользователя.

### Компиляция исходников

После перевода нужных строк их необходимо скомпилировать из формата `.po` в `.mo`, после чего перевод может быть использован в приложении и проекте:

```bash
django-admin compilemessages
```

Теперь, при смене `LANGUAGE_CODE` в настройках проекта на `"ru"` или `"ru-ru"`, при наличии соответствующих скомпилированных файлов локализации, указанные строки будут переведены на русский язык, остальные же строки просто остануться на английском.
