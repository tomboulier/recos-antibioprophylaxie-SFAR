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

      <!-- Footer simplifié au maximum pour correspond à l'image -->
      <div class="mt-20"></div>
      
      <div class="absolute bottom-0 w-full py-4 bg-white">
        <div class="max-w-4xl mx-auto flex items-center px-6">
          <div style="width: 60px">
            <img src="/logo_sfar.png" alt="SFAR" width="60" />
          </div>
          
          <div class="flex-1 ml-4 mr-4 text-left text-sm">
            <p>Recommandations formalisées d'experts de :</p>
            <p>• la Société Française d'Anesthésie-Réanimation (SFAR)</p>
            <p>• la Société de Pathologie Infectieuse de Langue Française (SPILF)</p>
          </div>
          
          <div style="width: 60px">
            <img src="/logo-SPILF.jpeg" alt="SPILF" width="60" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

