<script setup>
import { ref } from 'vue'
import SearchBar from './components/SearchBar.vue'
import InterventionList from './components/InterventionList.vue'
import { useLogger } from './services/logging.js'

// Initialisation du logger pour suivre les événements utilisateur
const logger = useLogger('App')

/**
 * État local de l'application
 */
const searchQuery = ref('')
const searchResults = ref([])

/**
 * Base de données d'interventions chirurgicales (simulation)
 * Dans une version réelle, ces données proviendraient d'un service métier
 */
const interventionsDb = [
  // Dérivations
  { id: 1, nom: 'Dérivation ventriculaire externe (DVE)' },
  { id: 2, nom: 'Dérivation lombaire externe (DLE)' },
  { id: 3, nom: 'Dérivation ventriculo-péritonéale (DVP)' },
  { id: 4, nom: 'Dérivation ventriculo-atriale (DVA)' },
  { id: 5, nom: 'Cystectomie sustrigonale partielle ou totale, quel que soit le mode de dérivation' },
  
  // Chirurgies digestives
  { id: 6, nom: 'Chirurgie gastro-duodénale' },
  { id: 7, nom: 'Chirurgie colo-rectale' },
  { id: 8, nom: 'Chirurgie hépato-biliaire' },
  { id: 9, nom: 'Chirurgie pancréatique' },
  
  // Chirurgies orthopédiques
  { id: 10, nom: 'Prothèse de hanche' },
  { id: 11, nom: 'Prothèse de genou' },
  { id: 12, nom: 'Chirurgie rachidienne' },
  { id: 13, nom: 'Arthroscopie' }
]

/**
 * Fonction pour gérer la recherche et mettre à jour les résultats
 * Implémente une recherche "fuzzy" simple basée sur des sous-chaînes
 */
const handleSearch = (query) => {
  searchQuery.value = query
  
  // Logge l'action utilisateur de recherche
  logger.info(`Recherche effectuée: "${query}"`)
  
  // Si la recherche est vide, réinitialiser les résultats
  if (query.trim() === '') {
    searchResults.value = []
    return
  }
  
  // Recherche insensible à la casse et aux accents
  const normalizedQuery = query.toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
  
  // Filtrage des interventions qui correspondent à la recherche
  searchResults.value = interventionsDb.filter(intervention => {
    const normalizedNom = intervention.nom.toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
    
    return normalizedNom.includes(normalizedQuery)
  })
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

