<script setup>
import { ref } from 'vue'
import HeaderApp from './components/HeaderApp.vue'
import FooterApp from './components/FooterApp.vue'
import SearchBar from './components/SearchBar.vue'
import InterventionList from './components/InterventionList.vue'

const searchQuery = ref('')
const searchResults = ref([])

// Fonction pour gérer la recherche et mettre à jour les résultats
const handleSearch = (query) => {
  searchQuery.value = query
  
  // Dans un premier temps, nous simulons les résultats
  // Plus tard, cela sera remplacé par un appel à l'API backend
  if (query.toLowerCase().includes('dérivation') || query.toLowerCase().includes('derivation')) {
    searchResults.value = [
      { id: 1, nom: 'Dérivation ventriculaire externe (DVE)' },
      { id: 2, nom: 'Dérivation lombaire externe (DLE)' },
      { id: 3, nom: 'Dérivation ventriculo-péritonéale (DVP)' },
      { id: 4, nom: 'Dérivation ventriculo-atriale (DVA)' },
    ]
  } else if (query.trim() === '') {
    searchResults.value = []
  } else {
    // Simulons quelques résultats pour toute autre recherche
    searchResults.value = [
      { id: 5, nom: 'Cystectomie sustrigonale partielle ou totale' },
    ]
  }
}
</script>

<template>
  <div class="min-h-screen bg-white p-4 md:p-6">
    <div class="max-w-xl mx-auto">
      <!-- En-tête de l'application -->
      <HeaderApp />

      <!-- Barre de recherche -->
      <SearchBar @search="handleSearch" />

      <!-- Liste des interventions trouvées -->
      <InterventionList 
        :interventions="searchResults" 
        :query="searchQuery"
      />

      <!-- Espacement pour que le contenu ne soit pas caché par le footer -->
      <div class="mb-24"></div>
      
      <!-- Footer STRICTEMENT horizontal avec display: flex et space-between -->      
      <div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 10px 0; border-top: 1px solid #eee;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 900px; margin: 0 auto; padding: 0 20px;">
          <!-- Logo gauche -->
          <img src="/logo_sfar.png" alt="SFAR" style="height: 40px; width: auto;" />
          
          <!-- Texte au milieu -->
          <div style="text-align: center; color: #333; font-size: 0.8rem; margin: 0 15px;">
            <p style="margin: 2px 0;">Recommandations formalisées d'experts de :</p>
            <p style="margin: 2px 0;">• la Société Française d'Anesthésie-Réanimation (SFAR)</p>
            <p style="margin: 2px 0;">• la Société de Pathologie Infectieuse de Langue Française (SPILF)</p>
          </div>
          
          <!-- Logo droite -->
          <img src="/logo-SPILF.jpeg" alt="SPILF" style="height: 40px; width: auto;" />
        </div>
      </div>
    </div>
  </div>
</template>

