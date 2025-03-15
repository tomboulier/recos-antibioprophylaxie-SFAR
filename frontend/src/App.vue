<script setup>
import { ref, onMounted } from 'vue'
import SearchBar from './components/SearchBar.vue'
import InterventionList from './components/InterventionList.vue'
import { useLogger } from './services/logging.js'
import { apiService } from './services/api.js'

// Initialisation du logger pour suivre les événements utilisateur
const logger = useLogger('App')

/**
 * État local de l'application
 */
const searchQuery = ref('')
const searchResults = ref([])
const isLoading = ref(false)
const hasError = ref(false)
const errorMessage = ref('')

/**
 * Fonction pour gérer la recherche et mettre à jour les résultats
 * Effectue une requête API vers le backend pour obtenir les résultats
 */
const handleSearch = async (query) => {
  searchQuery.value = query
  
  // Logge l'action utilisateur de recherche
  logger.info(`Recherche effectuée: "${query}"`)
  
  // Si la recherche est vide, réinitialiser les résultats
  if (query.trim() === '') {
    searchResults.value = []
    return
  }
  
  try {
    // Indique que la recherche est en cours
    isLoading.value = true
    hasError.value = false
    errorMessage.value = ''
    
    // Appel au service API pour obtenir les résultats
    const results = await apiService.searchProcedures(query)
    searchResults.value = results
    
    logger.info(`${results.length} interventions trouvées pour "${query}"`)
  } catch (error) {
    // Gestion des erreurs
    logger.error(`Erreur lors de la recherche: ${error.message}`)
    hasError.value = true
    errorMessage.value = `Une erreur est survenue lors de la recherche: ${error.message}`
    searchResults.value = []
  } finally {
    // Fin du chargement
    isLoading.value = false
  }
}
</script>

<template>
  <div style="width: 100%; min-height: 100vh; display: flex; flex-direction: column;">
    <!-- Header fixe en haut de page -->
    <div style="position: fixed; top: 0; left: 0; right: 0; background-color: white; z-index: 10; padding: 20px 0; border-bottom: 1px solid #f5f5f5;">
      <div style="text-align: center; max-width: 800px; margin: 0 auto;">
        <h1 style="font-size: 36px; font-weight: bold; margin-bottom: 2px;">Antibioprophylaxie</h1>
        <h2 style="font-size: 24px; margin-bottom: 0px; color: #333;">en chirurgie</h2>
        <h2 style="font-size: 24px; margin-bottom: 0px; color: #333;">et médecine interventionnelle</h2>
      </div>
    </div>
    
    <!-- Espace pour compenser le header fixe -->
    <div style="height: 120px;"></div>
    
    <!-- Zone principale pour la recherche et les résultats avec centrage vertical -->
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px;">
      <!-- Barre de recherche beaucoup plus large (maquette) -->
      <div style="width: 100%; max-width: 600px; margin: 0 auto; display: flex; justify-content: center; align-items: center;">
        <SearchBar @search="handleSearch" />
      </div>

      <!-- Indicateur de chargement -->
      <div v-if="isLoading" style="width: 100%; max-width: 600px; margin: 20px auto; text-align: center;">
        <p>Chargement des résultats...</p>
      </div>
      
      <!-- Message d'erreur -->
      <div v-if="hasError" style="width: 100%; max-width: 600px; margin: 20px auto; color: red; text-align: center;">
        <p>{{ errorMessage }}</p>
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

