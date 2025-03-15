<!-- 
  InterventionList.vue - Composant d'affichage des interventions chirurgicales trouvées
  
  Ce composant affiche la liste des interventions chirurgicales correspondant 
  à la recherche de l'utilisateur, avec une mise en valeur des termes recherchés.
 -->
<script setup>
import { computed } from 'vue'

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
 * Calcule s'il y a des résultats à afficher
 */
const hasResults = computed(() => props.interventions.length > 0)

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
 * Handler pour la sélection d'une intervention
 */
function handleInterventionClick(intervention) {
  // Cette fonction sera implémentée pour afficher les détails de l'intervention
  console.log('Intervention sélectionnée:', intervention)
}
</script>

<template>
  <!-- Container principal avec animation -->
  <div class="mt-4 transition-all duration-300">
    <!-- Message de statut de la recherche -->
    <div class="text-gray-600 text-sm mb-3" v-if="query || !hasResults">
      {{ resultMessage }}
    </div>
    
    <!-- Liste des interventions trouvées avec animation -->
    <transition-group 
      name="intervention-list" 
      tag="ul" 
      class="bg-white rounded-lg shadow-sm overflow-hidden"
      v-if="hasResults"
    >
      <li 
        v-for="intervention in interventions" 
        :key="intervention.id"
        class="border-b border-gray-100 last:border-b-0 transition-colors hover:bg-gray-50 cursor-pointer"
        @click="handleInterventionClick(intervention)"
      >
        <div class="p-4">
          <h3 class="text-lg text-gray-800">{{ intervention.nom }}</h3>
        </div>
      </li>
    </transition-group>
    
    <!-- État vide (pas de résultats) -->
    <div 
      v-if="!hasResults && query" 
      class="bg-white rounded-lg shadow-sm p-8 text-center text-gray-500"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p>Nous n'avons pas trouvé d'intervention correspondant à "{{ query }}"</p>
      <p class="text-sm mt-2">Essayez avec un autre terme ou vérifiez l'orthographe</p>
    </div>
  </div>
</template>

<style scoped>
/* Animations pour la liste d'interventions */
.intervention-list-enter-active,
.intervention-list-leave-active {
  transition: all 0.3s ease;
}
.intervention-list-enter-from,
.intervention-list-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
