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

from django.db import models
from core.models import StudentModel


# Notre modèle d'absence.
class StudentAbsenceModel(models.Model):
    # L'étudiant qui sera absent.
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date_absence_start = models.DateField("Date de début de l'absence")
    date_absence_end = models.DateField("Date de fin de l'absence")
    # Indique si l'étudiant est absent le matin.
    morning = models.BooleanField("Absence le matin", default=True)
    # Indique si l'étudiant est absent l'après-midi.
    afternoon = models.BooleanField("Absence l'après-midi", default=True)
    user = models.CharField("Utilisateur qui a créé l'absence", max_length=100)
    datetime_creation = models.DateTimeField("Date et heure de création de l'absence",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de l'absence",
                                           auto_now=True)
