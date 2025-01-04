<template>
  <div id="frequency-visualizer" class="w-full h-[50vh]"></div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import p5 from "p5";

const props = defineProps<{
  frequenciesData: number[];
}>();

const setupP5 = () => {
  new p5((p) => {
    let canvas;

    // Fréquences limites (pour l'échelle)
    const minFrequency = 20; // Fréquence basse (exemple : 20 Hz)
    const maxFrequency = 20000; // Fréquence haute (exemple : 20 kHz)

    // Intervalle de fréquence pour les paliers (ex : 100 Hz, 500 Hz, etc.)
    const frequencyIntervals = [
      20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000,
    ];

    p.setup = () => {
      canvas = p.createCanvas(p.windowWidth, p.windowHeight / 2);
      canvas.parent("frequency-visualizer");
    };

    p.draw = () => {
      p.background(23);

      // Dessiner le spectre de fréquence
      p.noStroke();
      p.fill(139, 92, 246);

      const barWidth = p.width / props.frequenciesData.length;

      // Dessiner les barres de fréquence
      props.frequenciesData.forEach((magnitude, index) => {
        // const x = index * barWidth;

        // Appliquer une échelle logarithmique pour l'axe X
        // Nous appliquons p.log pour étirer les basses fréquences et compresser les hautes fréquences
        const logX = p.map(
          p.log(index + 1),
          p.log(1),
          p.log(props.frequenciesData.length),
          0,
          p.width
        );

        const y = p.map(magnitude, 0, 1, p.height, p.height / 2); // Inverser la hauteur des barres
        p.rect(logX, y, barWidth, p.height - y);
      });

      // Ajouter l'échelle des fréquences sur l'axe X avec une échelle logarithmique
      p.fill(255);
      p.textAlign(p.CENTER, p.TOP);

      // Afficher les paliers de fréquence à intervalles spécifiques
      frequencyIntervals.forEach((freq, _i) => {
        // Appliquer le logarithme à la position X
        const freqPos = p.map(
          p.log(freq),
          p.log(minFrequency),
          p.log(maxFrequency),
          0,
          p.width
        );
        p.text(freq, freqPos, p.height - 30); // Afficher l'étiquette de fréquence
      });
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
