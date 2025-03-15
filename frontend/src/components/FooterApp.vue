<!-- 
  FooterApp.vue - Composant de pied de page de l'application
  Affiche les logos des sociétés savantes et les mentions
 -->
<template>
  <footer class="fixed bottom-0 w-full py-4 bg-white border-t border-gray-100">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between max-w-4xl mx-auto">
        <!-- Logo SFAR à gauche -->
        <div class="flex-shrink-0">
          <img src="/logo_sfar.png" alt="SFAR" class="h-10" />
        </div>
        
        <!-- Texte au centre -->
        <div class="text-center text-sm text-gray-700">
          <p>Recommandations formalisées d'experts de :</p>
          <p>• la Société Française d'Anesthésie-Réanimation (SFAR)</p>
          <p>• la Société de Pathologie Infectieuse de Langue Française (SPILF)</p>
        </div>
        
        <!-- Logo SPILF à droite -->
        <div class="flex-shrink-0">
          <img src="/logo-SPILF.jpeg" alt="SPILF" class="h-10" />
        </div>
      </div>
    </div>
  </footer>
</template>
