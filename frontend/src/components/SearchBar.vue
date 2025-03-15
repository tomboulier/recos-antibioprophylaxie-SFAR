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
  <div class="relative w-full mx-auto mb-4">
    <!-- Input de recherche large avec bordures parfaitement arrondies -->
    <div style="border: 1px solid #E5E7EB; border-radius: 50px; overflow: hidden; background-color: white; width: 100%; height: 56px; display: flex; align-items: center;">
      <input
        v-model="searchInput"
        type="text"
        placeholder="Rechercher une intervention"
        style="width: 100%; height: 100%; padding: 0 24px; border: none; outline: none; font-size: 16px; color: #333;"
        @input="handleSearch"
      />
    </div>
    
    <!-- Bouton de réinitialisation (X) visible uniquement quand il y a du texte -->
    <button 
      v-if="hasInput" 
      @click="clearSearch"
      style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #9CA3AF; z-index: 10;"
      aria-label="Effacer la recherche"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>
