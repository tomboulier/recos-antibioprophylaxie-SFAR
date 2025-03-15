<!-- 
  SearchBar.vue - Composant de recherche d'interventions chirurgicales
 -->
<script setup>
import { ref, watch } from 'vue'

// Modèle de données pour la requête de recherche
const searchInput = ref('')

// Événements du composant
const emit = defineEmits(['search'])

// Fonction qui déclenche l'événement de recherche vers le parent
function handleSearch() {
  emit('search', searchInput.value)
}

// Mise à jour en temps réel
watch(searchInput, (newValue) => {
  emit('search', newValue)
})
</script>

<template>
  <div class="w-full max-w-md mx-auto mb-8">
    <div class="relative">
      <input
        v-model="searchInput"
        type="text"
        placeholder="Rechercher une intervention"
        class="w-full px-4 py-2 border border-gray-300 rounded-md text-gray-800 shadow-sm
               focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400"
        @input="handleSearch"
      />
    </div>
  </div>
</template>
