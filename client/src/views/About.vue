<template>
  <v-container>
    <v-col>
      <v-card elevation="2">
        <v-card-title>API Request Example</v-card-title>
        <v-card-text>{{ text }}</v-card-text>
        <v-card-actions>
          <v-btn text color="teal" @click="sendRequest">Submit Request</v-btn>
          <v-btn text color="teal" @click="resetText">Reset Request</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-col>
      <comment-form />
    </v-col>
    <v-col>
      <comments-card />
    </v-col>
  </v-container>
</template>

<script>
import CommentForm from "../components/CommentForm.vue";
import CommentsCard from "../components/CommentsCard.vue";
import axios from "axios";

export default {
  components: {
    CommentForm,
    CommentsCard,
  },
  data: () => {
    return {
      text: "Send a request to change this text",
    };
  },
  methods: {
    sendRequest() {
      axios
        .get(process.env.VUE_APP_API_ENDPOINT + "/api/sample")
        .then((response) => (this.text = response.data));
    },
    resetText() {
      this.text = "Send a request to change this text";
    },
  },
};
</script>

