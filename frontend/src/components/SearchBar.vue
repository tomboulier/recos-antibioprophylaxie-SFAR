<!-- 
  SearchBar.vue - Composant de recherche d'interventions chirurgicales
  Affiche une barre de recherche pour les interventions avec autocomplétion
 -->
<script setup>
import { ref, watch, computed } from 'vue'

/**
 * Modèle de données pour la requête de recherche
 */
const searchInput = ref('')

/**
 * Événements du composant
 */
const emit = defineEmits(['search'])

/**
 * Détermine si un texte est présent dans la recherche
 */
const hasInput = computed(() => searchInput.value.trim().length > 0)

/**
 * Fonction qui déclenche l'événement de recherche vers le parent
 */
function handleSearch() {
  emit('search', searchInput.value)
}

/**
 * Efface le contenu de la recherche
 */
function clearSearch() {
  searchInput.value = ''
  emit('search', '')
}

/**
 * Mise à jour en temps réel de la recherche
 */
watch(searchInput, (newValue) => {
  emit('search', newValue)
})
</script>

<template>
  <div class="relative w-full max-w-md mx-auto mb-4">
    <!-- Input de recherche avec bordures arrondies -->
    <input
      v-model="searchInput"
      type="text"
      placeholder="Rechercher une intervention"
      class="w-full px-4 py-3 bg-white border border-gray-200 rounded-full text-gray-800 shadow-sm text-base
            focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400"
      @input="handleSearch"
    />
    
    <!-- Bouton de réinitialisation (X) visible uniquement quand il y a du texte -->
    <button 
      v-if="hasInput" 
      @click="clearSearch"
      class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
      aria-label="Effacer la recherche"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>
