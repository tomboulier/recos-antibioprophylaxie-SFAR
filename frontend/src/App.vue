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
  <div style="width: 100%; height: 100vh; display: flex; flex-direction: column;">
    <!-- Zone principale centrée verticalement et horizontalement -->
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 0 20px;">
      <!-- Titre et sous-titres absolument centrés -->
      <div style="text-align: center; margin-bottom: 50px;">
        <h1 style="font-size: 48px; font-weight: bold; margin-bottom: 16px;">Antibioprophylaxie</h1>
        <h2 style="font-size: 28px; margin-bottom: 8px;">en chirurgie</h2>
        <h2 style="font-size: 28px; margin-bottom: 40px;">et médecine interventionnelle</h2>
      </div>

      <!-- Barre de recherche -->
      <div style="width: 100%; max-width: 500px; margin: 0 auto;">
        <SearchBar @search="handleSearch" />
      </div>

      <!-- Liste des interventions trouvées -->
      <div style="width: 100%; max-width: 600px; margin: 20px auto;">
        <InterventionList 
          :interventions="searchResults" 
          :query="searchQuery"
        />
      </div>
    </div>
    
    <!-- Footer horizontal avec flexbox -->
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
</template>

