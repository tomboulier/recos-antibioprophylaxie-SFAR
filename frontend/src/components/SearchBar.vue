<!-- 
  SearchBar.vue - Composant de recherche d'interventions chirurgicales
  
  Ce composant implémente une barre de recherche réactive qui émet les événements 
  de recherche vers le composant parent pour permettre le filtrage des interventions.
 -->
<script setup>
import { ref, watch } from 'vue'

/**
 * Modèle de données pour la requête de recherche
 */
const searchInput = ref('')

/**
 * Props et événements du composant
 */
const emit = defineEmits(['search'])

/**
 * Fonction qui déclenche l'événement de recherche vers le parent
 */
function handleSearch() {
  emit('search', searchInput.value)
}

/**
 * Surveille les changements de l'entrée utilisateur pour mettre à jour 
 * les résultats de recherche en temps réel
 */
watch(searchInput, (newValue) => {
  emit('search', newValue)
})
</script>

<template>
  <div class="relative mb-6">
    <!-- Champ de recherche avec style minimaliste et moderne -->
    <input
      v-model="searchInput"
      type="text"
      placeholder="Rechercher une intervention"
      class="w-full px-5 py-4 bg-white rounded-lg shadow-sm text-gray-800 
             focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
      @input="handleSearch"
    />
    
    <!-- Icône de recherche -->
    <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
  </div>
</template>
