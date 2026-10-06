# Les Délices de Gnamienssa — Site vitrine & commande

Site statique HTML / CSS / JS (aucune dépendance). Ouvre `index.html` dans un navigateur.

## Structure
```
index.html
assets/
  css/style.css      → design system + styles
  js/config.js       → numéro WhatsApp + URL API backend
  js/data.js         → catalogue (plats, formules, suppléments)
  js/main.js         → rendu, panier (localStorage), checkout
  images/            → photos des plats
```

## Commande
1. Le client ajoute des plats au panier.
2. Il remplit le formulaire (nom, téléphone, livraison/retrait, date, paiement).
3. La commande est envoyée sur WhatsApp, et en POST JSON vers `API_URL` si renseigné.

## Brancher le backend
Dans `assets/js/config.js`, renseigne `API_URL`. Payload envoyé :
```json
{ "ref": "GN-XXXX", "customer": { "name", "phone", "mode", "address", "date", "payment", "note" },
  "items": [{ "id", "name", "qty", "unitPrice" }], "total": 0, "createdAt": "ISO" }
```
Pistes : endpoint `/orders`, paiement Mobile Money (CinetPay, PayDunya, Wave), et remplacer `data.js` par un `GET /products`.
⚠️ Toujours recalculer le total côté serveur.
