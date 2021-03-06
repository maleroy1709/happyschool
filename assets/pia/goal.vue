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
        <b-card>
            <b-form-row>
                <b-col>
                    <strong>
                        <b-form inline>
                            Du<b-form-input
                                type="date"
                                v-model="date_start"
                                class="mr-sm-2 ml-2"
                            />
                            au<b-form-input
                                type="date"
                                v-model="date_end"
                                class="ml-2"
                            />
                        </b-form>
                    </strong>
                </b-col>
                <b-col
                    cols="4"
                    align-self="end"
                >
                    <b-btn
                        @click="toggleExpand"
                        variant="light"
                    >
                        {{ expanded ? "Cacher" : "Voir" }}
                    </b-btn>
                    <b-btn
                        @click="$emit('remove')"
                        variant="danger"
                    >
                        Supprimer
                    </b-btn>
                </b-col>
            </b-form-row>
            <b-collapse
                v-model="expanded"
                :id="Math.random().toString(36).substring(7)"
            >
                <b-form-row class="mt-2">
                    <b-col>
                        <b-form-group
                            label="Objectif transversal"
                            label-cols="3"
                        >
                            <multiselect
                                :options="crossGoalOptions"
                                placeholder="Choisisser un ou des objectifs"
                                tag-placeholder="Ajouter un nouvel objectif"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="crossGoal"
                                :show-no-options="false"
                                @tag="addCrossGoalTag"
                                label="goal"
                                track-by="goal"
                                multiple
                                taggable
                            >
                                <span slot="noResult">Aucun aménagements trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group
                            label="Indicateur(s)/Action(s)"
                            label-cols="2"
                        >
                            <quill-editor
                                v-model="indicatorAction"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group
                            label="Aide(s)"
                            label-cols="2"
                        >
                            <quill-editor
                                v-model="givenHelp"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group label="Auto-évaluation">
                            <quill-editor
                                v-model="selfAssessment"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group label="Évaluation">
                            <multiselect
                                :options="assessmentOptions"
                                placeholder="Choisisser une ou des évaluations"
                                tag-placeholder="Ajouter l'évaluation"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="assessment"
                                :show-no-options="false"
                                label="assessment"
                                track-by="id"
                            >
                                <span slot="noResult">Aucune évaluation trouvée.</span>
                                <span slot="noOptions" />
                            </multiselect>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-row>
                    <b-col>
                        <b-btn
                            @click="subGoals.unshift({})"
                            variant="info"
                        >
                            Ajouter un objectif de branche
                        </b-btn>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <subgoal
                            v-for="(subgoal, index) in subGoals"
                            :key="subgoal.id"
                            :subgoal="subgoal"
                            ref="subgoals"
                            class="mt-2"
                            @remove="removeSubGoal(index)"
                        />
                    </b-col>
                </b-row>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

import Subgoal from "./subgoal.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        goal: {
            type: Object,
            default: () => {},
        },
        pia_model: {
            type: Number,
            default: -1,
        },
        showExpanded: {
            type: Boolean,
            default: false,
        }
    },
    data: function () {
        return {
            date_start: null,
            date_end: null,
            crossGoalOptions: [],
            crossGoal: [],
            givenHelp: "",
            indicatorAction: "",
            selfAssessment: "",
            assessmentOptions: [],
            assessment: null,
            editorOptions: {
                modules: {
                    toolbar: [
                        ["bold", "italic", "underline", "strike"],
                        ["blockquote"],
                        [{ "list": "ordered"}, { "list": "bullet" }],
                        [{ "indent": "-1"}, { "indent": "+1" }],
                        [{ "align": [] }],
                        ["clean"]
                    ]
                },
                placeholder: ""
            },
            subGoals: [],
            expanded: false,
        };
    },
    methods: {
        toggleExpand: function () {
            this.expanded = !this.expanded;
        },
        removeSubGoal: function (subGoalIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer l'objectif de branche ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app.goal.id < 0 || !("id" in app.subGoals[subGoalIndex])) {
                        app.subGoals.splice(subGoalIndex, 1);
                    } else {
                        axios.delete("/pia/api/subgoal/" + app.subGoals[subGoalIndex].id + "/", token)
                            .then(() => app.subGoals.splice(subGoalIndex, 1))
                            .catch(err => alert(err));
                    }
                    
                }
            });
        },
        assignGoal: function () {
            if (this.goal.id >= 0) {
                this.date_start = this.goal.date_start;
                this.date_end = this.goal.date_end;
                this.indicatorAction = this.goal.indicator_action;
                this.givenHelp = this.goal.given_help;
                this.selfAssessment = this.goal.self_assessment;
                this.assessment = this.assessmentOptions.filter(a => a.id == this.goal.assessment)[0];

                // Assign crossGoals
                let goals = this.goal.cross_goals.split(";");
                this.crossGoal = this.crossGoalOptions.filter(cg => goals.includes(cg.goal));
                let newGoals = goals.filter(g => !this.crossGoalOptions.map(cg => cg.goal).includes(g));
                newGoals.forEach(ng => this.addCrossGoalTag(ng));
            }
        },
        addCrossGoalTag: function (tag) {
            this.crossGoal.push({id: -1, goal: tag});
        },
        submit: function (piaId) {
            if (this.goal) {
                const crossGoals = this.crossGoal.reduce((acc, cg) => acc + ";" + cg.goal, "");
                const data = {
                    pia_model: piaId,
                    date_start: this.date_start,
                    date_end: this.date_end,
                    indicator_action: this.indicatorAction,
                    given_help: this.givenHelp,
                    self_assessment: this.selfAssessment,
                    assessment: this.assessment.id,
                    cross_goals: this.crossGoal.length > 0 ? crossGoals.slice(1) : null,
                };

                const isNew = this.goal.id < 0;
                const url =  !isNew ? "/pia/api/goal/" + this.goal.id + "/" : "/pia/api/goal/";
                return !isNew ? axios.put(url, data, token) : axios.post(url, data, token);
            }
        },
        submitSubGoal: function (goalId) {
            // Check if there is at least one subgoal.
            if (this.subGoals.length == 0) return [];

            return this.$refs.subgoals.map(sg => sg.submit(goalId));
        }
    },
    mounted: function () {
        if (this.goal.id < 0) this.expanded = true;

        const promises = [
            axios.get("/pia/api/cross_goal/"),
            axios.get("/pia/api/assessment/"),
        ];
        if (this.goal.id >= 0) promises.push(axios.get("/pia/api/subgoal/?goal=" + this.goal.id));
        Promise.all(promises)
            .then(resps => {
                this.crossGoalOptions = resps[0].data.results;
                this.assessmentOptions = resps[1].data.results;
                this.assignGoal();
                if (this.goal.id >= 0) this.subGoals = resps[2].data.results;
            });
    },
    components: {
        Multiselect,
        quillEditor,
        Subgoal,
    }
};
</script>
