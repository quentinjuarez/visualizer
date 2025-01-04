<template>
  <div class="p-4 bg-neutral-800 rounded-md shadow-md text-white">
    <h2 class="text-xl font-bold">Audio Info</h2>
    <div class="mt-2">
      <p><strong>Amplitude (Peak):</strong> {{ peakAmplitude }}</p>
      <p><strong>Average Volume:</strong> {{ averageVolume }}</p>
      <p><strong>Data Points:</strong> {{ audioData.length }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  audioData: number[];
}>();

// Compute the peak amplitude
const peakAmplitude = computed(() => {
  if (props.audioData.length === 0) return 0;
  return Math.max(...props.audioData.map(Math.abs));
});

// Compute the average volume
const averageVolume = computed(() => {
  if (props.audioData.length === 0) return 0;
  const sum = props.audioData.reduce((acc, value) => acc + Math.abs(value), 0);
  return Math.round(sum / props.audioData.length);
});
</script>
