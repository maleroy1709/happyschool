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

import json

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters import rest_framework as filters

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.views import BaseModelViewSet, BaseFilters
from core.models import ResponsibleModel
from core.people import get_classes
from core.utilities import get_menu


from student_absence.models import StudentAbsenceModel, StudentAbsenceSettingsModel
from student_absence.serializers import StudentAbsenceSerializer, StudentAbsenceSettingsSerializer


def get_settings():
    settings_student_absence = StudentAbsenceSettingsModel.objects.first()
    if not settings_student_absence:
        # Create default settings.
        StudentAbsenceSettingsModel.objects.create().save()

    return settings_student_absence


class StudentAbsenceView(LoginRequiredMixin,
                         TemplateView):
    template_name = "student_absence/student_absence.html"
    filters = [
        {'value': 'student_id', 'text': 'Matricule'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'date_absence_start', 'text': 'Début absence'},
        {'value': 'date_absence_end', 'text': 'Fin absence'},
    ]

    def get_context_data(self, **kwargs):
        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context['menu'] = json.dumps(get_menu(self.request.user, "student_absence"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((StudentAbsenceSettingsSerializer(get_settings()).data))
        return context


class StudentAbsenceFilter(BaseFilters):
    classe = filters.CharFilter(method='classe_by')

    class Meta:
        fields_to_filter = ('student_id', 'date_absence_start', 'date_absence_end')
        model = StudentAbsenceModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def classe_by(self, queryset, name, value):
        if not value[0].isdigit():
            return queryset

        teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
        classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
        queryset = queryset.filter(student__classe__in=classes)

        if len(value) > 0:
            queryset = queryset.filter(student__classe__year=value[0])
            if len(value) > 1:
                queryset = queryset.filter(student__classe__letter=value[1].lower())
        return queryset


class StudentAbsenceViewSet(BaseModelViewSet):
    queryset = StudentAbsenceModel.objects.filter(student__isnull=False)

    serializer_class = StudentAbsenceSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = StudentAbsenceFilter
    ordering_fields = ('datetime_creation',)
