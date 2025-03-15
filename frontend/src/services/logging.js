/**
 * Service de journalisation des événements applicatifs
 * 
 * Ce service fournit des fonctionnalités de journalisation uniformes pour toute l'application
 * en respectant les principes de Domain Driven Design et SOLID.
 */

/**
 * Implémentation du journal en console
 * 
 * Cette implémentation envoie les messages au logger de la console
 */
class JournalConsole {
  /**
   * Crée une nouvelle instance de journal console
   * 
   * @param {string} contexte - Le contexte d'où provient ce journal (nom du composant/service)
   */
  constructor(contexte) {
    this.contexte = contexte;
  }
  
  /**
   * Formate un message avec le contexte et l'heure actuelle
   * 
   * @param {string} message - Le message à formater
   * @returns {string} Le message formaté
   */
  formaterMessage(message) {
    const horodatage = new Date().toISOString();
    return `[${horodatage}] [${this.contexte}] ${message}`;
  }
  
  /**
   * Enregistre un message de niveau information
   * 
   * @param {string} message - Le message à journaliser
   */
  info(message) {
    console.log(this.formaterMessage(message));
  }
  
  /**
   * Enregistre un message de niveau avertissement
   * 
   * @param {string} message - Le message à journaliser
   */
  avertissement(message) {
    console.warn(this.formaterMessage(message));
  }
  
  /**
   * Enregistre un message de niveau erreur
   * 
   * @param {string} message - Le message à journaliser
   */
  erreur(message) {
    console.error(this.formaterMessage(message));
  }
}

/**
 * Crée une instance de journal adaptée au contexte d'utilisation
 * 
 * Pattern Factory pour créer des instances de Journal
 * 
 * @param {string} contexte - Le contexte d'utilisation (nom du composant, service, etc.)
 * @returns {Object} Une instance de journal configurée
 */
export function useLogger(contexte) {
  // Actuellement, nous utilisons toujours JournalConsole,
  // mais cette factory permettra de changer l'implémentation facilement
  return new JournalConsole(contexte);
}
