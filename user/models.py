from django.db import models
from datetime import date, timedelta


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name="Язык программирования")
    month_to_learn = models.IntegerField(verbose_name="Продолжительность курса")

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.month_to_learn}'


class AbstractPerson(models.Model):
    name = models.CharField(max_length=30, verbose_name="ФИО человека")
    email = models.CharField(max_length=30, verbose_name="Почта", unique=True)
    phone_number = models.CharField(max_length=13, verbose_name="номер телефона")

    def save(self, *args, **kwargs):
            if self.phone_number.startswith('0'):
                self.phone_number = '+996' + self.phone_number[1:]
            super(AbstractPerson, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.email}- {self.phone_number}'

    class Meta:
        abstract = True


class Student(AbstractPerson):
    work_study_place = models.CharField(max_length=30, null=True, blank=True, verbose_name="Место учебы/работы")
    has_own_notebook = models.BooleanField(verbose_name="Есть ли свой ноутбук")
    preferred_os = models.CharField(max_length=30, verbose_name="Предпочитаемая операционная система", choices=(
        ('windows', 'Windows'),
        ('macos', 'MacOS'),
        ('linux', 'Linux'),
    ))

    def __str__(self):
        return f'{self.work_study_place} - {self.has_own_notebook}- {self.preferred_os}'


class Mentor(AbstractPerson):
    main_work = models.CharField(max_length=30, null=True, blank=True, verbose_name="основное место работы ")
    experience = models.DateField(verbose_name="дата начала работы программистом ")
    courses = models.ManyToManyField(Student, related_name="mentors", through="Course", verbose_name="Курс")

    def __str__(self):
        return f'{self.main_work} - {self.experience}- {self.courses}'


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name="Наименование курса")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Язык программирования")
    date_started = models.DateField(default=date.today, verbose_name="Дата начала курсов")
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name="Ментор")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")

    def get_end_date(self):
        duration_months = self.language.month_to_learn
        end_date = self.date_started + timedelta(days=30*duration_months)
        if self.date_started.day > 15:
            end_date += timedelta(days=15)
        return end_date

    def __str__(self):
        return f'{self.name} - {self.language}- {self.date_started} - {self.mentor} - {self.student}'

