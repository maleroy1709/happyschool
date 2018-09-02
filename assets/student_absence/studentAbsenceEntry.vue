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
        <transition appear name="fade">
            <b-card>
                <b-row>
                    <b-col><strong><a href="#" @click="filterStudent">{{ rowData.student.display }}</a> : </strong>
                    Absent du {{ rowData.date_absence_start }} au {{ rowData.date_absence_end}}.</b-col>
                    <b-col sm="2"><div class="text-right">
                        <b-btn variant="light" size="sm" @click="editEntry" class="card-link">
                            <icon scale="1.3" name="edit" color="green" class="align-text-bottom"></icon>
                        </b-btn>
                        <b-btn variant="light" size="sm" @click="deleteEntry"class="card-link">
                            <icon scale="1.3" name="trash" color="red" class="align-text-bottom"></icon>
                        </b-btn>
                    </div></b-col>
                </b-row>
            </b-card>
        </transition>
    </div>
</template>

<script>
export default {
    props: {
        rowData : {type: Object},
    },
    data: function () {
        return {
        }
    },
    methods: {
        deleteEntry: function () {
            this.$emit('delete');
        },
        editEntry: function () {
            this.$emit('edit');
        },
        filterStudent: function () {
            this.$emit('filterStudent', this.rowData.student_id);
        }
    }
}
</script>

<style>
.fade-enter-active {
  transition: opacity .7s
}
.fade-enter, .fade-leave-to .fade-leave-active {
  opacity: 0
}
</style>
