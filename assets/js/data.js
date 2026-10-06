/**
 * Catalogue produits. Remplaçable plus tard par un GET depuis ton backend.
 * price = prix "à partir de" en francs CFA.
 */
window.PRODUCTS = [
  { id: "garba", name: "Attiéké Garba", cat: "attieke", price: 1000, img: "assets/images/garba.jpg", desc: "Attiéké accompagné de poisson, oignon, tomate et condiments." },
  { id: "attieke-poisson", name: "Attiéké + poisson braisé", cat: "attieke", price: 2000, img: "assets/images/attieke-poisson.jpg", desc: "Poisson braisé accompagné d'attiéké, d'oignon, tomate et condiments." },
  { id: "attieke-poulet", name: "Attiéké + poulet braisé", cat: "attieke", price: 2500, img: "assets/images/attieke-poulet.jpg", desc: "Poulet braisé accompagné d'attiéké et de ses garnitures." },
  { id: "tchep-poulet", name: "Tchèp au poulet", cat: "riz", price: 2000, img: "assets/images/tchep-poulet.jpg", desc: "Riz préparé avec légumes et poulet." },
  { id: "tchep-poisson", name: "Tchèp au poisson", cat: "riz", price: 2000, img: "assets/images/tchep-poisson.jpg", desc: "Riz préparé avec légumes et poisson." },
  { id: "abolo", name: "Abolo", cat: "tradition", price: 1000, img: "assets/images/abolo.jpg", desc: "Abolo accompagné de sa garniture et de son accompagnement au choix." },
  { id: "foufou", name: "Foufou", cat: "tradition", price: 2000, img: "assets/images/foufou.jpg", desc: "Foufou accompagné d'une sauce savoureuse." },
];

window.FORMULES = [
  { id: "petite-famille", name: "Petite famille", people: "3 personnes", price: 5000 },
  { id: "famille", name: "Famille", people: "4 à 5 personnes", price: 8000, featured: true },
  { id: "grande-famille", name: "Grande famille", people: "6 à 8 personnes", price: 10000 },
];

window.SUPPLEMENTS = [
  { id: "sup-attieke", name: "Portion d'attiéké", price: 500 },
  { id: "sup-riz", name: "Portion de riz", price: 500 },
  { id: "sup-poisson", name: "Poisson supplémentaire", price: 1000 },
  { id: "sup-poulet", name: "Poulet supplémentaire", price: 1000 },
  { id: "sup-alloco", name: "Alloco", price: 500 },
  { id: "sup-oeuf", name: "Œuf", price: 200 },
  { id: "sup-sauce", name: "Sauce supplémentaire", price: 300 },
  { id: "sup-boisson", name: "Boisson", price: 500 },
];
