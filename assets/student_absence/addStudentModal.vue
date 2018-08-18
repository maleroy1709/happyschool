<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
<div>
    <b-modal size="lg" title="Nouvelle absence"
        ok-title="Soumettre" cancel-title="Annuler"
        ref="addStudentModal"
        >
        <b-form>
            <b-form-row>
                <b-col sm="8">
                    <b-form-group label="Étudiant :" label-for="input-student" :state="inputStates.student">
                        <multiselect id="input-name"
                            :internal-search="false"
                            :options="studentOptions"
                            @search-change="getStudentOptions"
                            :loading="studentLoading"
                            placeholder="Rechercher un étudiant…"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label=""
                            label="display"
                            track-by="matricule"
                            v-model="student"
                            >
                            <span slot="noResult">Aucune personne trouvée.</span>

                        </multiselect>
                        <span slot="invalid-feedback">{{ errorMsg('student_id') }}</span>
                    </b-form-group>
                </b-col>
                <b-col sm="4">
                    <b-form-group label="Matricule :" label-for="input-matricule">
                        <b-form-input id="input-matricule" type="text" v-model="student.matricule" readonly></b-form-input>
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row class="mt-4">
                <b-col>
                    <b-form-row>
                        <b-form-group label="À partir du">
                            <input type="date" v-model="form.date_absence_start" :max="form.date_absence_end" />
                        </b-form-group>
                    </b-form-row>
                </b-col>
                <b-col>
                    <b-form-row>
                        <b-form-group label="Jusqu'au">
                            <input type="date" v-model="form.date_absence_end" :min="form.date_absence_start" />
                        </b-form-group>
                    </b-form-row>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-form-group label="Matin/Après-midi :">
                        <b-form-checkbox v-model="form.morning">
                            Matin
                        </b-form-checkbox>
                        <b-form-checkbox v-model="form.afternoon">
                            Après-midi
                        </b-form-checkbox>
                </b-form-group>
            </b-form-row>
        </b-form>
    </b-modal>
</div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

export default {
    props: ['entry'],
    data: function () {
        return {
            form: {
                matricule_id: null,
                date_absence_start: null,
                date_absence_end: null,
                morning: true,
                afternoon: true,
            },
            student: {matricule: null},
            studentOptions: [],
            studentLoading: false,
            inputStates: {
                student: null,
            },
            errors: {},
            searchId: -1,
        }
    },
    watch: {
        'form.date_absence_start': function (date) {
            if (this.form.date_absence_end === null) this.form.date_absence_end = date;
        },
    },
    methods: {
        show: function () {
            this.$refs.addStudentModal.show();
        },
        hide: function () {
            this.$refs.addStudentModal.hide();
        },
        getStudentOptions: function (query) {
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.studentLoading = true;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: 'student',
                check_access: false,
            };
            axios.post('/annuaire/api/people/', data, token)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;

                const options = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                    // It's a student.
                    entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                    entry.display += " – " + p.teaching.display_name;
                    return entry;
                });
                this.studentLoading = false;
                this.studentOptions = options;
            })
            .catch(function (error) {
                alert(error);
                app.studentLoading = false;
            });
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
    },
    components: {Multiselect},
    mounted: function () {
        this.show();
    },
}
</script>
