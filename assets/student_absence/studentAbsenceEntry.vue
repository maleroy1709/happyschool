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
                <strong>{{ rowData.student.display }} : </strong>
                Absent du {{ rowData.date_absence_start }} au {{ rowData.date_absence_end}}.
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
