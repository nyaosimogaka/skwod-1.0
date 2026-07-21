<template>
  <v-app>

    <v-app-bar>
      <v-app-bar-title>
        SKWOD Admin
      </v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer permanent>
      <v-list nav>

        <v-list-item
          title="Dashboard"
          prepend-icon="mdi-view-dashboard"
          to="/"
        />

        <v-list-item
          title="Sports"
          prepend-icon="mdi-basketball"
          to="/sports"
        />

        <v-list-item
          title="Countries"
          prepend-icon="mdi-earth"
          to="/countries"
        />

      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>