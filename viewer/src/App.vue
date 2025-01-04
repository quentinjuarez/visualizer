<template>
  <div class="flex flex-col h-screen bg-neutral-900 text-white">
    <Wave :audioData="audioData" />
    <Freq :frequenciesData="frequenciesData" />
    <AudioInfo :audioData="audioData" class="absolute top-4 right-4 min-w-96" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Wave from "./components/Wave.vue";
import AudioInfo from "./components/AudioInfo.vue";
import Freq from "./components/Freq.vue";

const ws = ref<WebSocket>();
const audioData = ref([]);
const frequenciesData = ref([]);

// WebSocket connection
const setupWebSocket = () => {
  ws.value = new WebSocket("ws://localhost:8765");

  ws.value.onopen = () => {
    console.log("Connected to WebSocket server.");
  };

  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.audio) {
      audioData.value = data.audio;
      frequenciesData.value = data.frequencies;
    }
  };

  ws.value.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  ws.value.onclose = () => {
    console.log("WebSocket connection closed.");
  };
};

onMounted(() => {
  setupWebSocket();
});
</script>

<style>
body {
  @apply bg-gray-900;
}
</style>
