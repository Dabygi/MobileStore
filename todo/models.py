from __future__ import unicode_literals

import datetime
import os
import textwrap

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import DEFAULT_DB_ALIAS, models
from django.db.transaction import Atomic, get_connection
from django.urls import reverse
from django.utils import timezone


def get_attachment_upload_dir(instance, filename):
    """Determine upload dir for task attachment files.

    Определите каталог загрузки для файлов вложений задач.
    """

    return "/".join(["tasks", "attachments", str(instance.task.id), filename])


class LockedAtomicTransaction(Atomic):
    """
    modified from https://stackoverflow.com/a/41831049
    this is needed for safely merging

    Does a atomic transaction, but also locks the entire table for any transactions, for the duration of this
    transaction. Although this is the only way to avoid concurrency issues in certain situations, it should be used with
    caution, since it has impacts on performance, for obvious reasons...

    модификации для https://stackoverflow.com/a/41831049 это необходимо для безопасного слияния.

    Выполняет атомарную транзакцию, но также блокирует всю таблицу для любых транзакций на время этой транзакции.
    Хотя это единственный способ избежать проблем с параллелизмом в определенных ситуациях,
    его следует использовать с осторожностью, поскольку по очевидным причинам он влияет на производительность...
    """

    def __init__(self, *models, using=None, savepoint=None):
        if using is None:
            using = DEFAULT_DB_ALIAS
        super().__init__(using, savepoint)
        self.models = models

    def __enter__(self):
        super(LockedAtomicTransaction, self).__enter__()

        # Make sure not to lock, when postgresql is used, or you'll run into problems while running tests!!!
        # Убедитесь, что не заблокирован, когда используется postgresql, иначе вы столкнетесь с проблемами при выполнении тестов!!!
        if settings.DATABASES[self.using]["ENGINE"] != "django.db.backends.postgresql_psycopg2":
            cursor = None
            try:
                cursor = get_connection(self.using).cursor()
                for model in self.models:
                    cursor.execute(
                        "LOCK TABLE {table_name}".format(table_name=model._meta.db_table)
                    )
            finally:
                if cursor and not cursor.closed:
                    cursor.close()


class TaskList(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(default="")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"

        # Prevents (at the database level) creation of two lists with the same slug in the same group
        unique_together = ("group", "slug")


class Task(models.Model):
    title = models.CharField(max_length=140)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(default=timezone.now, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="todo_created_by",
        on_delete=models.CASCADE,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="todo_assigned_to",
        on_delete=models.CASCADE,
    )
    note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)

    # Has due date for an instance of this object passed?
    # Прошел ли срок для экземпляра этого объекта?
    def overdue_status(self):
        "Returns whether the Tasks's due date has passed or not."
        "Возвращает, прошел ли срок выполнения задачи или нет."
        if self.due_date and datetime.date.today() > self.due_date:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo:task_detail", kwargs={"task_id": self.id})

    # Auto-set the Task creation / completed date
    # Автоматическая установка даты создания/завершения задачи
    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        # Если задача помечена как завершенная, установите значение completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    def merge_into(self, merge_target):
        if merge_target.pk == self.pk:
            raise ValueError("can't merge a task with self")

        # lock the comments to avoid concurrent additions of comments after the
        # update request. these comments would be irremediably lost because of
        # the cascade clause

        # заблокируйте комментарии, чтобы избежать одновременного добавления комментариев после запроса на обновление.
        # эти комментарии были бы безвозвратно утеряны из-за каскадного условия.
        with LockedAtomicTransaction(Comment):
            Comment.objects.filter(task=self).update(task=merge_target)
            self.delete()

    class Meta:
        ordering = ["priority", "created_date"]


class Comment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.

    Не используем встроенные комментарии Django, потому что мы хотим иметь возможность сохранять
    комментарии и одновременно изменять детали задачи. Пробрасываем наши собственные, так как это легко.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="todo_comments"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
    email_from = models.CharField(max_length=320, blank=True, null=True)
    email_message_id = models.CharField(max_length=255, blank=True, null=True)

    body = models.TextField(blank=True)

    class Meta:
        # an email should only appear once per task
        # электронное письмо должно появляться только один раз для каждой задачи
        unique_together = ("task", "email_message_id")

    @property
    def author_text(self):
        if self.author is not None:
            return str(self.author)

        assert self.email_message_id is not None
        return str(self.email_from)

    @property
    def snippet(self):
        body_snippet = textwrap.shorten(self.body, width=35, placeholder="...")
        # Define here rather than in __str__ so we can use it in the admin list_display
        # Определите здесь, а не в __str__, чтобы мы могли использовать его в отображении списка администраторов
        return "{author} - {snippet}...".format(author=self.author_text, snippet=body_snippet)

    def __str__(self):
        return self.snippet


class Attachment(models.Model):
    """
    Defines a generic file attachment for use in M2M relation with Task.

    Определяет общее вложение файла для использования в связи M2M с задачей.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    file = models.FileField(upload_to=get_attachment_upload_dir, max_length=255)

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def __str__(self):
        return f"{self.task.id} - {self.file.name}"
