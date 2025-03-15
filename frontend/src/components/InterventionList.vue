<!-- 
  InterventionList.vue - Composant d'affichage des interventions chirurgicales trouvées
  
  Ce composant affiche la liste des interventions chirurgicales correspondant 
  à la recherche de l'utilisateur, avec une mise en valeur des termes recherchés.
 -->
<script setup>
import { computed, ref } from 'vue'

/**
 * Props du composant
 */
const props = defineProps({
  // Liste des interventions à afficher
  interventions: {
    type: Array,
    required: true,
    default: () => []
  },
  // Requête de recherche actuelle
  query: {
    type: String,
    required: false,
    default: ''
  }
})

/**
 * État d'ouverture du panneau de résultats
 */
const isOpen = ref(true)

/**
 * Calcule s'il y a des résultats à afficher et si la recherche est active
 */
const hasResults = computed(() => props.interventions.length > 0)
const isSearchActive = computed(() => props.query && props.query.trim().length > 0)

/**
 * Calcule le message à afficher en fonction des résultats et de la recherche
 */
const resultMessage = computed(() => {
  if (!props.query) {
    return 'Commencez à taper pour rechercher une intervention'
  }
  
  if (!hasResults.value) {
    return `Aucune intervention trouvée pour "${props.query}"`
  }
  
  return props.interventions.length === 1 
    ? '1 intervention trouvée'
    : `${props.interventions.length} interventions trouvées`
})

/**
 * Ferme la fenêtre des résultats
 */
function closeResults() {
  isOpen.value = false
}

/**
 * Handler pour la sélection d'une intervention
 */
function handleInterventionClick(intervention) {
  // Cette fonction sera implémentée pour afficher les détails de l'intervention
  console.log('Intervention sélectionnée:', intervention)
}

/**
 * Met en évidence les termes de recherche dans le texte
 */
function highlightMatch(text, query) {
  if (!query || !text) return text
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<span class="highlight">$1</span>')
}
</script>

<template>
  <!-- Container principal avec animation -->
  <div class="relative w-full transition-all duration-300 max-w-md mx-auto">
    <!-- Boîte de résultats avec bordure et ombre similaire à l'image partagée -->
    <div 
      v-if="isSearchActive && isOpen"
      class="absolute left-0 right-0 top-0 bg-white rounded-xl border border-gray-200 shadow-lg overflow-hidden z-10"
    >
      <!-- Barre supérieure avec la requête et bouton fermer -->
      <div class="flex justify-between items-center px-4 py-3 bg-gray-50 border-b border-gray-200">
        <span class="font-medium text-gray-700">{{ query }}</span>
        <button @click="closeResults" class="text-gray-500 hover:text-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Liste des interventions trouvées avec animation -->
      <transition-group 
        name="intervention-list" 
        tag="ul" 
        class="divide-y divide-gray-100 max-h-80 overflow-y-auto"
        v-if="hasResults"
      >
        <li 
          v-for="intervention in interventions" 
          :key="intervention.id"
          class="py-3 px-4 transition-colors hover:bg-gray-50 cursor-pointer"
          @click="handleInterventionClick(intervention)"
        >
          <div v-html="highlightMatch(intervention.nom, query)" class="text-base text-gray-800"></div>
        </li>
      </transition-group>
      
      <!-- État vide (pas de résultats) -->
      <div 
        v-if="!hasResults && isSearchActive" 
        class="p-6 text-center text-gray-500"
      >
        <p class="text-gray-500">Aucun résultat pour "{{ query }}"</p>
        <p class="text-sm mt-1 text-gray-400">Essayez avec un autre terme</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Animations pour la liste d'interventions avec une transition douce */
.intervention-list-enter-active,
.intervention-list-leave-active {
  transition: all 0.2s ease;
}
.intervention-list-enter-from,
.intervention-list-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

/* Style pour la mise en évidence des termes recherchés */
:deep(.highlight) {
  font-weight: bold;
  color: #000;
}
</style>
