<template>
    <div>
        <b-navbar
            toggleable="lg"
            type="light"
            variant="light"
        >
            <b-nav-toggle target="nav_text_collapse" />
            <b-navbar-brand href="/">
                <img
                    id="logo-school"
                    src="/static/img/logo_school.png"
                    class="d-inline-block align-top"
                >
                HappySchool
            </b-navbar-brand>
            <b-collapse
                is-nav
                id="nav_text_collapse"
            >
                <b-navbar-nav
                    is-nav-bar
                    v-for="(app) in menuInfo.apps"
                    :key="app.app"
                >
                    <b-nav-item
                        :active="app.active"
                        :href="app.url"
                    >
                        {{ app.display }}
                    </b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-text><strong>{{ menuInfo.full_name }}</strong></b-nav-text>
                    <b-nav-item-dropdown
                        text="Options"
                        right
                    >
                        <b-dropdown-item href="/core/profil/">
                            Profil
                        </b-dropdown-item>
                        <b-dropdown-item
                            v-if="menuInfo.admin_settings"
                            href="/core/admin/"
                        >
                            Administration
                        </b-dropdown-item>
                        <b-dropdown-divider />
                        <b-dropdown-item href="/logout/">
                            Se déconnecter
                        </b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
export default {
    props: {
        "menu-info":{
            type: Object,
            default: () => {}
        }
    },
    data: function () {
        return {
        };
    },
};
</script>

<style>
#logo-school {
    max-height: 35px;
}
</style>
