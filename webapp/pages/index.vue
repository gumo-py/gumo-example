<template>
  <section class="container">
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">Gumo Task Emulator</b-navbar-brand>
        </b-navbar>

        <b-container>
            <b-row>
                <b-col>
                    <h2>Cloud Tasks Local Emulator Console</h2>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-button variant="light">Refresh</b-button>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-table striped hover :items="items" />
                </b-col>
            </b-row>

            <b-row>
                <div>
                    {{asyncData}}
                </div>
            </b-row>
        </b-container>
    </div>
  </section>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
    components: {
        Logo
    },

    async asyncData({ $axios }) {
        const ip = await $axios.$get('http://icanhazip.com');
        return { ip }
    },

    data() {
        return {
            items: [
                { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
            ]
        }
    }
}
</script>

<style>
</style>
