/**
 * Service de journalisation des événements applicatifs
 * 
 * Ce service fournit des fonctionnalités de journalisation uniformes pour toute l'application
 * en respectant les principes de Domain Driven Design et SOLID.
 */

/**
 * Interface définissant un journal d'application
 * 
 * Conforme au principe d'inversion des dépendances (DIP) du SOLID
 */
export interface Journal {
  /**
   * Enregistre un message de niveau information
   * 
   * Parameters
   * ----------
   * message : string
   *     Le message à journaliser
   */
  info(message: string): void;
  
  /**
   * Enregistre un message de niveau avertissement
   * 
   * Parameters
   * ----------
   * message : string
   *     Le message à journaliser
   */
  avertissement(message: string): void;
  
  /**
   * Enregistre un message de niveau erreur
   * 
   * Parameters
   * ----------
   * message : string
   *     Le message à journaliser
   */
  erreur(message: string): void;
}

/**
 * Implémentation du journal en console
 * 
 * Cette implémentation envoie les messages au logger de la console
 */
class JournalConsole implements Journal {
  private contexte: string;
  
  /**
   * Crée une nouvelle instance de journal console
   * 
   * Parameters
   * ----------
   * contexte : string
   *     Le contexte d'où provient ce journal (nom du composant/service)
   */
  constructor(contexte: string) {
    this.contexte = contexte;
  }
  
  /**
   * Formate un message avec le contexte et l'heure actuelle
   */
  private formaterMessage(message: string): string {
    const horodatage = new Date().toISOString();
    return `[${horodatage}] [${this.contexte}] ${message}`;
  }
  
  /**
   * Enregistre un message de niveau information
   */
  info(message: string): void {
    console.log(this.formaterMessage(message));
  }
  
  /**
   * Enregistre un message de niveau avertissement
   */
  avertissement(message: string): void {
    console.warn(this.formaterMessage(message));
  }
  
  /**
   * Enregistre un message de niveau erreur
   */
  erreur(message: string): void {
    console.error(this.formaterMessage(message));
  }
}

/**
 * Crée une instance de journal adaptée au contexte d'utilisation
 * 
 * Pattern Factory pour créer des instances de Journal
 * 
 * Parameters
 * ----------
 * contexte : string
 *     Le contexte d'utilisation (nom du composant, service, etc.)
 * 
 * Returns
 * -------
 * Journal
 *     Une instance de journal configurée
 */
export function useLogger(contexte: string): Journal {
  // Actuellement, nous utilisons toujours JournalConsole,
  // mais cette factory permettra de changer l'implémentation facilement
  return new JournalConsole(contexte);
}
