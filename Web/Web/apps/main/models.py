from django.db import models

class Worker(models.Model):
    first_name = models.CharField('имя', max_length=50)
    last_name = models.CharField('фамилия', max_length=50)
    login = models.CharField('логин', max_length=50)
    password = models.CharField('паспорт', max_length=50)
    email = models.CharField('емейл', max_length=50)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'