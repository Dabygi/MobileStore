# The integrated mail queue functionality can enable advanced functionality if
# django-autocomplete-light is installed and configured. We can use this module
# to check for other installed dependencies in the future.

# Встроенная функция очереди почты может включать расширенные функциональные возможности,
# если установлен и настроен django-autocomplete-light.
# Мы можем использовать этот модуль для проверки других установленных зависимостей в будущем.

HAS_AUTOCOMPLETE = True
try:
    import dal
except ImportError:
    HAS_AUTOCOMPLETE = False

HAS_TASK_MERGE = False
if HAS_AUTOCOMPLETE:
    import dal.autocomplete

    if getattr(dal.autocomplete, "Select2QuerySetView", None) is not None:
        HAS_TASK_MERGE = True
