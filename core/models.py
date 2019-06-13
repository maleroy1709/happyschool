# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

import requests

from django.conf import settings
from django.db import models

from .ldap import get_ldap_connection
from .serializers import TeachingSerializer, ClasseSerializer


class CoreSettingsModel(models.Model):
    root = models.URLField("Root URL", help_text='URL vers le serveur HappySchool principal',
                               blank=True, null=True, default=None)
    remote = models.URLField("Remote URL", help_text='URL vers un serveur HappySchool distant',
                             blank=True, null=True, default=None)
    remote_token = models.CharField(max_length=50, help_text="Token généré sur le serveur distant",
                                    blank=True, null=True, default=None)


class RemoteModel(models.Model):
    model_url = ""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_insert, using, update_fields)
        sync_remote = False
        if sync_remote:
            _copy_to_remote(self, TeachingSerializer, self.model_url)

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        sync_remote = False
        if sync_remote:
            _delete_remote(self, self.model_url)


class TeachingModel(RemoteModel):
    model_url = "core/api/teaching/"

    display_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100, help_text="Nom simple pour la programmation.")

    def __str__(self):
        return "%s (%s)" % (self.display_name, self.name)


class ClasseModel(RemoteModel):
    model_url = "core/api/classe/"
    year = models.IntegerField()
    letter = models.CharField(max_length=20)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.year) + self.letter.upper() + " – " + str(self.teaching.display_name)

    @property
    def compact_str(self):
        return str(self.year) + self.letter.upper()


class StudentModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    matricule = models.PositiveIntegerField(unique=True, primary_key=True)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)
    classe = models.ForeignKey(ClasseModel, on_delete=models.SET_NULL,
                               null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True, blank=True)
    inactive_from = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        """Return the full name with the last name first."""
        if self.inactive_from:
            return '%s %s (%s)' % (self.last_name, self.first_name, 'ancien')
        else:
            return '%s %s %s' % (self.last_name, self.first_name, str(self.classe))

    @property
    def fullname(self):
        return '%s %s' % (self.last_name, self.first_name)

    @property
    def fullname_classe(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.classe.compact_str)

    @property
    def display(self):
        return self.__str__()



class AdditionalStudentInfo(models.Model):
    student = models.OneToOneField(StudentModel, primary_key=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True)
    scholar_year = models.CharField(max_length=9, blank=True)
    previous_classe = models.CharField(max_length=20, blank=True)
    orientation = models.CharField(max_length=200, blank=True)

    birth_date = models.DateField("birth date", null=True, blank=True)
    street = models.CharField(max_length=500, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    locality = models.CharField(max_length=200, blank=True)

    student_phone = models.CharField(max_length=100, blank=True)
    student_mobile = models.CharField(max_length=100, blank=True)
    student_email = models.EmailField(null=True, blank=True)

    resp_last_name = models.CharField(max_length=200, blank=True)
    resp_first_name = models.CharField(max_length=200, blank=True)
    resp_phone = models.CharField(max_length=100, blank=True)
    resp_mobile = models.CharField(max_length=100, blank=True)
    resp_email = models.EmailField(null=True, blank=True)

    father_last_name = models.CharField(max_length=200, blank=True)
    father_first_name = models.CharField(max_length=200, blank=True)
    father_job = models.CharField(max_length=500, blank=True)
    father_phone = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=100, blank=True)
    father_email = models.EmailField(null=True, blank=True)

    mother_last_name = models.CharField(max_length=200, blank=True)
    mother_first_name = models.CharField(max_length=200, blank=True)
    mother_job = models.CharField(max_length=500, blank=True)
    mother_phone = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=100, blank=True)
    mother_email = models.EmailField(null=True, blank=True)

    doctor = models.CharField(max_length=200, blank=True)
    doctor_phone = models.CharField(max_length=200, blank=True)
    mutual = models.CharField(max_length=200, blank=True)
    mutual_number = models.CharField(max_length=200, blank=True)
    medical_information = models.CharField(max_length=500, blank=True)

    username = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=20, blank=True)


class ResponsibleModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    matricule = models.BigIntegerField(blank=True, null=True, unique=True)
    teaching = models.ManyToManyField(TeachingModel, blank=True)
    email = models.EmailField(blank=True, null=True)
    email_school = models.EmailField(blank=True, null=True)
    classe = models.ManyToManyField(ClasseModel, default=None, blank=True)
    tenure = models.ManyToManyField(ClasseModel,
                               blank=True,
                               default=None,
                               related_name="tenure_classe")
    is_teacher = models.BooleanField(default=False)
    is_educator = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    inactive_from = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        """Return the full name with the last name first."""
        return "%s %s" % (self.last_name, self.first_name)

    @property
    def fullname(self):
        return '%s %s' % (self.last_name, self.first_name)

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def password(self) -> str:
        if settings.USE_LDAP_INFO:
            password = self._get_ldap_properties()[settings.AUTH_LDAP_USER_ATTR_MAP['password']]
            if type(password) == list:
                password = password[0]
            return password
        else:
            return self.user.password

    def _get_ldap_properties(self):
        if settings.USE_LDAP_INFO:
            connection = get_ldap_connection()
            base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
            # Assume username is unique.
            ldap_username_attr = settings.AUTH_LDAP_USER_ATTR_MAP['username']
            connection.search(base_dn, "(%s=%s)" % (ldap_username_attr, self.user.username),
                              attributes='*')
            if len(connection.response) > 0:
                return connection.response[0]['attributes']

            raise Exception("Teacher not found in the LDAP directory.")
        else:
            return None

    @property
    def display(self):
        return self.__str__()


class YearModel(models.Model):
    year = models.IntegerField("year")

    def __str__(self):
        return str(self.year)


class EmailModel(models.Model):
    email = models.EmailField()
    display = models.CharField(max_length=300, default="")
    teaching = models.ForeignKey(TeachingModel, on_delete=models.SET_NULL, null=True, blank=True)
    is_pms = models.BooleanField(default=False)
    years = models.ManyToManyField(YearModel, blank=True)

    def __str__(self):
        return self.display


class ImportCalendarModel(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(help_text="URL du calendrier ics.")

    def __str__(self):
        return self.name


def _get_remote_settings() -> dict:
    core_settings = CoreSettingsModel.objects.first()
    remote_url = core_settings.remote
    # Ensure a slash at the end.
    if remote_url[-1] != '/':
        remote_url += '/'
    remote_token = core_settings.remote_token
    headers = {'Authorization': 'Token %s' % remote_token}
    return {"remote_url": remote_url, "headers": headers}


def _copy_to_remote(instance, serializer, url):
    remote_settings = _get_remote_settings()
    remote_url = remote_settings["remote_url"]
    remote_url += url
    method = requests.post if instance.pk else requests.put
    if method != requests.post:
        remote_url += '%i/' % instance.pk
    instance.request.data = serializer(instance).data
    method(remote_url, headers=remote_settings["headers"], json=instance.request.data)


def _delete_remote(instance, url):
    remote_settings = _get_remote_settings()
    remote_url = remote_settings["remote_url"]
    remote_url += url
    remote_url += '%i/' % instance.pk
    requests.delete(remote_url, headers=remote_settings["headers"])