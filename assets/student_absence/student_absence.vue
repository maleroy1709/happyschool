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
        <div class="loading" v-if="!loaded"></div>
        <app-menu :menu-info="menuInfo"></app-menu>
        <b-container v-if="loaded">
            <b-row>
                <h2>Absence des élèves</h2>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <b-btn variant="primary" @click="openDynamicModal('add-student-modal')">
                                <icon name="plus" scale="1" class="align-middle"></icon>
                                Nouvelle absence
                            </b-btn>
                            <b-btn variant="outline-secondary" v-b-toggle.filters>
                                <icon name="search" scale="1"></icon>
                                Ajouter des filtres
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-collapse id="filters" v-model="showFilters">
                        <b-card>
                            <filters app="student_absence" model="student_absence" ref="filters" @update="applyFilter"></filters>
                        </b-card>
                    </b-collapse>
                </b-col>
            </b-row>
            <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
            </b-pagination>
            <b-row>
                <b-col>
                    <student-absence-entry
                    v-for="(entry, index) in entries"
                    v-bind:key="entry.id"
                    v-bind:row-data="entry"
                        >
                    </student-absence-entry>
                </b-col>
            </b-row>
        </b-container>
        <component
            v-bind:is="currentModal" ref="dynamicModal"
            @update="loadEntries">
        </component>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';

import Filters from '../common/filters.vue'
import Menu from '../common/menu.vue'

import StudentAbsenceEntry from './studentAbsenceEntry.vue'
import AddStudentModal from './addStudentModal.vue'

export default {
    data: function () {
        return {
            menuInfo: {},
            currentPage: 1,
            entriesCount: 0,
            entries: [],
            filter: '',
            ordering: '&ordering=-datetime_creation',
            loaded: false,
            showFilters: false,
            currentModal: '',
        }
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            if ('dynamicModal' in this.$refs) this.$refs.dynamicModal.show();
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.$store.state.filters
            for (let f in storeFilters) {
                if (storeFilters[f].filterType.startsWith("date")
                    || storeFilters[f].filterType.startsWith("time")) {
                    let ranges = storeFilters[f].value.split("_");
                    this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                } else {
                    this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                }
            }
            this.currentPage = 1;
            this.loadEntries();
        },
        loadEntries: function () {
            // Get current absences.
            axios.get('/student_absence/api/student_absence/?page=' + this.currentPage + this.filter + this.ordering)
            .then(response => {
                this.entriesCount = response.data.count;
                this.entries = response.data.results;
                // Everything is ready, hide the loading icon and show the content.
                this.loaded = true;
            });
        }
    },
    mounted: function () {
        this.menuInfo = menu;

        this.loadEntries();
    },
    components: {
        'filters': Filters,
        'app-menu': Menu,
        'student-absence-entry': StudentAbsenceEntry,
        'add-student-modal': AddStudentModal,
    },
}
</script>

<style>
.loading {
  content: " ";
  display: block;
  position: absolute;
  width: 80px;
  height: 80px;
  background-image: url(/static/img/spin.svg);
  background-size: cover;
  left: 50%;
  top: 50%;
}
</style>
