/**
 * Service API pour communiquer avec le backend
 * Permet de rechercher des interventions chirurgicales et autres opérations liées aux données
 */

import { useLogger } from './logging.js'

const logger = useLogger('ApiService')

// Configuration de base de l'API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Service pour interagir avec l'API backend
 */
export const apiService = {
  /**
   * Recherche des interventions chirurgicales par nom
   * 
   * @param {string} query - Terme de recherche (min 3 caractères)
   * @returns {Promise<Array>} Liste des interventions correspondantes
   */
  async searchProcedures(query) {
    if (!query || query.trim().length < 3) {
      logger.warn('La recherche nécessite au moins 3 caractères')
      return []
    }
    
    try {
      logger.info(`Appel API: recherche d'interventions avec le terme "${query}"`)
      const response = await fetch(`${API_BASE_URL}/procedures/search/by-name?name=${encodeURIComponent(query)}`)
      
      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status} ${response.statusText}`)
      }
      
      const data = await response.json()
      logger.info(`${data.length} résultats trouvés pour "${query}"`)
      
      // Transformation des données du backend vers le format utilisé dans le frontend
      return data.map(procedure => ({
        id: procedure.id,
        nom: procedure.name
      }))
    } catch (error) {
      logger.error(`Erreur lors de la recherche d'interventions: ${error.message}`)
      throw error
    }
  },
  
  /**
   * Récupère les détails d'une intervention chirurgicale spécifique
   * 
   * @param {number} id - Identifiant de l'intervention
   * @returns {Promise<Object>} Détails de l'intervention
   */
  async getProcedureDetails(id) {
    try {
      logger.info(`Appel API: récupération des détails de l'intervention ${id}`)
      const response = await fetch(`${API_BASE_URL}/procedures/${id}`)
      
      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status} ${response.statusText}`)
      }
      
      const data = await response.json()
      logger.info(`Détails récupérés pour l'intervention ${id}`)
      
      return data
    } catch (error) {
      logger.error(`Erreur lors de la récupération des détails: ${error.message}`)
      throw error
    }
  }
}
