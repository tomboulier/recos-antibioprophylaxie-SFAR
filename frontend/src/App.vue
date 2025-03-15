<script setup>
import { ref } from 'vue'
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
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="max-w-3xl mx-auto">
      <!-- Header avec le titre principal -->
      <header class="text-center mb-12 mt-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Antibioprophylaxie</h1>
        <h2 class="text-3xl font-semibold text-gray-800 mb-2">en chirurgie</h2>
        <h3 class="text-2xl font-medium text-gray-700">et médecine interventionnelle</h3>
      </header>

      <!-- Barre de recherche -->
      <SearchBar @search="handleSearch" />

      <!-- Liste des interventions trouvées -->
      <InterventionList 
        :interventions="searchResults" 
        :query="searchQuery"
      />

      <!-- Footer avec logos et mentions -->
      <footer class="mt-20 flex flex-col md:flex-row items-center justify-center space-y-6 md:space-y-0 md:space-x-8">
        <div class="flex items-center justify-center">
          <img src="/logo_sfar.png" alt="SFAR" class="h-16" />
        </div>
        <div class="text-sm text-gray-600 max-w-sm text-center md:text-left">
          <p class="font-medium mb-2">Recommandations formalisées d'experts de :</p>
          <ul class="list-disc pl-5 mt-1 space-y-1">
            <li>la Société Française d'Anesthésie-Réanimation (SFAR)</li>
            <li>la Société de Pathologie Infectieuse de Langue Française (SPILF)</li>
          </ul>
        </div>
        <div class="flex items-center justify-center">
          <img src="/logo-SPILF.jpeg" alt="SPILF" class="h-16" />
        </div>
      </footer>
    </div>
  </div>
</template>

