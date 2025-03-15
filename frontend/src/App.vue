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

      <!-- Espace pour les résultats de recherche -->
      <div class="mb-20"></div>
      
      <!-- Pied de page de l'application -->
      <FooterApp />
    </div>
  </div>
</template>

