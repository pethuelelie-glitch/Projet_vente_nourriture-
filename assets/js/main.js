(() => {
  const C = window.APP_CONFIG;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const fmt = (n) => n.toLocaleString("fr-FR").replace(/\u202f|\u00a0/g, " ") + " " + C.CURRENCY;
  const ALL = [...PRODUCTS, ...FORMULES, ...SUPPLEMENTS];
  const find = (id) => ALL.find((p) => p.id === id);

  /* ---------- Rendu ---------- */
  const grid = $("#menuGrid");
  function renderMenu(filter = "all") {
    grid.innerHTML = PRODUCTS.filter((p) => filter === "all" || p.cat === filter)
      .map((p, i) => `
      <article class="card reveal" style="--d:${i * 70}ms">
        <div class="card__media"><img src="${p.img}" alt="${p.name}" loading="lazy" width="816" height="816"/>
          <span class="card__price">dès ${fmt(p.price)}</span></div>
        <div class="card__body">
          <h3>${p.name}</h3>
          <p>${p.desc}</p>
          <button class="btn btn--dark btn--full" data-add="${p.id}">Ajouter au panier <span>+</span></button>
        </div>
      </article>`).join("");
    observe();
  }
  $("#formulesGrid").innerHTML = FORMULES.map((f) => `
    <article class="formule reveal ${f.featured ? "is-featured" : ""}">
      ${f.featured ? '<span class="badge">Le + choisi</span>' : ""}
      <h3>${f.name}</h3>
      <p class="formule__people">${f.people}</p>
      <p class="formule__price"><small>à partir de</small>${fmt(f.price)}</p>
      <button class="btn ${f.featured ? "btn--gold" : "btn--ghost"} btn--full" data-add="${f.id}">Choisir</button>
    </article>`).join("");
  $("#suppList").innerHTML = SUPPLEMENTS.map((s) => `
    <li class="supp"><span>${s.name}</span><em>${fmt(s.price)}</em>
      <button class="icon-btn icon-btn--gold" data-add="${s.id}" aria-label="Ajouter ${s.name}">+</button></li>`).join("");

  $("#filters").addEventListener("click", (e) => {
    const b = e.target.closest("[data-filter]"); if (!b) return;
    $$(".chip").forEach((c) => c.classList.toggle("is-active", c === b));
    renderMenu(b.dataset.filter);
  });

  /* ---------- Panier ---------- */
  let cart = JSON.parse(localStorage.getItem("gnam_cart") || "{}");
  const save = () => { localStorage.setItem("gnam_cart", JSON.stringify(cart)); renderCart(); };
  const total = () => Object.entries(cart).reduce((s, [id, q]) => s + (find(id)?.price || 0) * q, 0);

  function renderCart() {
    const entries = Object.entries(cart).filter(([id]) => find(id));
    const count = entries.reduce((s, [, q]) => s + q, 0);
    const cc = $("#cartCount"); cc.textContent = count;
    cc.classList.remove("bump"); void cc.offsetWidth; cc.classList.add("bump");
    $("#cartList").innerHTML = entries.map(([id, q]) => {
      const p = find(id);
      return `<li class="line">
        ${p.img ? `<img src="${p.img}" alt=""/>` : `<div class="line__ph">${p.name[0]}</div>`}
        <div class="line__info"><b>${p.name}</b><small>${fmt(p.price)}</small></div>
        <div class="qty"><button data-dec="${id}">−</button><span>${q}</span><button data-inc="${id}">+</button></div>
      </li>`;
    }).join("");
    $("#cartEmpty").hidden = count > 0;
    $("#cartFoot").hidden = count === 0;
    $("#cartTotal").textContent = $("#checkoutTotal").textContent = fmt(total());
  }

  document.addEventListener("click", (e) => {
    const add = e.target.closest("[data-add]");
    if (add) { const id = add.dataset.add; cart[id] = (cart[id] || 0) + 1; save(); toast(`${find(id).name} ajouté ✓`); }
    const inc = e.target.closest("[data-inc]"); if (inc) { cart[inc.dataset.inc]++; save(); }
    const dec = e.target.closest("[data-dec]");
    if (dec) { const id = dec.dataset.dec; cart[id]--; if (cart[id] <= 0) delete cart[id]; save(); }
    if (e.target.closest("[data-close]")) closeDrawer();
  });

  /* ---------- Drawer ---------- */
  const drawer = $("#drawer"), overlay = $("#overlay");
  const step = (name) => ["Cart", "Checkout", "Done"].forEach((s) => ($("#step" + s).hidden = s !== name));
  const openDrawer = () => { step("Cart"); drawer.classList.add("is-open"); overlay.classList.add("is-open"); };
  const closeDrawer = () => { drawer.classList.remove("is-open"); overlay.classList.remove("is-open"); };
  $("#openCart").onclick = openDrawer; $("#closeCart").onclick = closeDrawer; overlay.onclick = closeDrawer;
  $("#toCheckout").onclick = () => step("Checkout");
  $("#backToCart").onclick = () => step("Cart");
  $("#doneClose").onclick = closeDrawer;
  document.addEventListener("keydown", (e) => e.key === "Escape" && closeDrawer());

  const form = $("#stepCheckout");
  form.addEventListener("change", () => { $("#addrField").hidden = form.mode.value !== "Livraison"; });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    const items = Object.entries(cart).map(([id, qty]) => ({ id, name: find(id).name, qty, unitPrice: find(id).price }));
    const order = { ref: "GN-" + Date.now().toString(36).toUpperCase(), customer: data, items, total: total(), createdAt: new Date().toISOString() };

    if (!C.API_URL) {
      toast("Erreur : l'API de paiement n'est pas configurée.");
      return;
    }
    
    try { 
      const res = await fetch(C.API_URL, { 
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify(order) 
      }); 
      
      if (!res.ok) throw new Error("Erreur serveur");
      const respData = await res.json();
      
      // On vide le panier avant de partir
      cart = {}; save(); form.reset();

      if (respData.payment_url) {
          window.location.href = respData.payment_url;
      } else {
          // Si pour une raison quelconque on n'a pas d'URL (ou mock désactivé), on affiche l'étape final
          step("Done");
          $("#orderRef").textContent = order.ref;
          if (respData.receipt_url) {
              const receiptUrl = window.location.origin.replace('5500', '8000') + respData.receipt_url;
              const btn = document.createElement("a");
              btn.href = receiptUrl;
              btn.target = "_blank";
              btn.className = "btn btn--ghost btn--full";
              btn.style.marginTop = "15px";
              btn.textContent = "Télécharger le reçu PDF";
              $("#stepDone .drawer__body").appendChild(btn);
          }
      }
    }
    catch (err) { 
      console.error(err);
      toast("Erreur lors de la communication avec le serveur."); 
    }
  });

  /* ---------- UI ---------- */
  let tt; function toast(t) { const el = $("#toast"); el.textContent = t; el.classList.add("is-on"); clearTimeout(tt); tt = setTimeout(() => el.classList.remove("is-on"), 1800); }
  const io = new IntersectionObserver((es) => es.forEach((x) => x.isIntersecting && (x.target.classList.add("is-in"), io.unobserve(x.target))), { threshold: 0.15 });
  function observe() { $$(".reveal:not(.is-in)").forEach((el) => io.observe(el)); }
  window.addEventListener("scroll", () => {
    $("#nav").classList.toggle("is-solid", scrollY > 40);
    $(".hero__bg img").style.transform = `scale(1.08) translateY(${scrollY * 0.15}px)`;
  }, { passive: true });
  $("#year").textContent = new Date().getFullYear();

  renderMenu(); renderCart(); observe();
})();
