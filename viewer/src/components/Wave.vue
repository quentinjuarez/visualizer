<template>
  <div id="visualizer" class="w-full h-[50vh]"></div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import p5 from "p5";

const props = defineProps<{
  audioData: number[];
}>();

// p5.js sketch
const setupP5 = () => {
  new p5((p) => {
    let canvas;

    p.setup = () => {
      canvas = p.createCanvas(p.windowWidth, p.windowHeight / 2);
      canvas.parent("visualizer");
    };

    p.draw = () => {
      p.background(23);
      p.noFill();
      // purple
      p.stroke(139, 92, 246);

      const waveform = props.audioData;

      // Map and draw waveform
      p.beginShape();
      waveform.forEach((value, index) => {
        const x = p.map(index, 0, waveform.length, 0, p.width);
        const y = p.map(value, -32768, 32767, p.height, 0);
        p.vertex(x, y);
      });
      p.endShape();
    };

    p.windowResized = () => {
      p.resizeCanvas(p.windowWidth, p.windowHeight / 2);
    };
  });
};

onMounted(() => {
  setupP5();
});
</script>
