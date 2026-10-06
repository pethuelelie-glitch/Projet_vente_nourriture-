/**
 * Configuration — à adapter.
 * WHATSAPP_NUMBER : numéro au format international sans "+" ni espaces.
 * API_URL : quand ton backend est prêt, mets l'URL de l'endpoint (ex: "https://api.monsite.com/orders").
 *           Le site enverra un POST JSON { ref, customer, items, total, createdAt }.
 *           Si vide, la commande est envoyée uniquement via WhatsApp.
 */
window.APP_CONFIG = {
  WHATSAPP_NUMBER: "2250700000000",
  API_URL: "",
  CURRENCY: "F",
};
