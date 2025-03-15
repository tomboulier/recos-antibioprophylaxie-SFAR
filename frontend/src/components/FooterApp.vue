<!-- 
  FooterApp.vue - Composant de pied de page de l'application
  Affiche les logos des sociétés savantes et les mentions
 -->
<template>
  <footer class="fixed bottom-4 w-full left-0 right-0 flex flex-col items-center text-center text-gray-600">
    <div class="flex space-x-8 items-center">
      <img src="/logo_sfar.png" alt="SFAR" class="h-12 opacity-90" />
      <div class="text-sm max-w-sm">
        <p class="font-medium mb-1">Recommandations formalisées d'experts de :</p>
        <p>• la Société Française d'Anesthésie-Réanimation (SFAR)</p>
        <p>• la Société de Pathologie Infectieuse de Langue Française (SPILF)</p>
      </div>
      <img src="/logo-SPILF.jpeg" alt="SPILF" class="h-12 opacity-90" />
    </div>
  </footer>
</template>
