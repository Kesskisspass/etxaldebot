selected_products = []

function choose_prod(){
  // On récupère le contenu de l'option selectionnée du select
  var sel = document.getElementById("select_prod");
  var prod_txt = sel.options[sel.selectedIndex].text;

  // On crée un élément de liste et on l'ajoute dans le dom en ciblant l'ul parent
  li = document.createElement("li")
  li.classList.add("bg-primary","rounded-pill","text-white","m-1","pl-3","pr-3", "d-inline-block")
  li.innerHTML = prod_txt
  target = document.getElementById("selected_prod")
  target.appendChild(li)

  // On ajoute également l'id du produit dans un array pour faire notre requete recommandation
  selected_products.push(prod_txt)

  // On active si necessaire le bouton pour effacer la liste
  var delete_list_btn = document.getElementById("delete_list_btn")
  delete_list_btn.disabled = false;

  // Si plus de trois produits dans le "panier" on peux activer le bouton recommandation
  if(selected_products.length>=3) {
    var reco_btn = document.getElementById("recommandation_btn")
    reco_btn.disabled = false
  }
}

function delete_liste_prod() {

  // Si user efface la liste on efface les elements du dom et on vide notre array
  target = document.getElementById("selected_prod")
  while (target.firstChild) {
    target.removeChild(target.lastChild);
  }

  // On supprime les recommandations
  reco = document.getElementById("display_recommandation")
  while (reco.firstChild) {
    reco.removeChild(reco.lastChild);
  }
  // On vide la liste des produits selectionnés
  selected_products = []

  // Et on remet les boutons dans leur état initial
  var delete_list_btn = document.getElementById("delete_list_btn")
  delete_list_btn.disabled = true;
  var reco_btn = document.getElementById("recommandation_btn")
  reco_btn.disabled = true
}

// Fonction qui génère le second select à partir de la catégorie choisie
function get_cat_id() {
    cat_id = document.getElementById("cat_id").value;
    console.log(cat_id);

    fetch('http://127.0.0.1:5000/get_product', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({categorie:cat_id}),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function (response) {

        if (response.status !== 200) {
            console.log("Erreur ! Response status: " + response.status);
            return ;
          }
          response.json().then(function(data) {

            console.log("Data reçues :",data);

            // Création du select
            var target = document.getElementById("select_product")
            while (target.firstChild) {
                target.removeChild(target.lastChild);
              }
            var elt = document.createElement("label")
            elt.innerHTML = "Choisir le produit"
            var select = document.createElement("select")
            select.id = "select_prod"
            select.classList.add("form-control","mx-auto","col-9")
            select.setAttribute("onchange","choose_prod()")
            var opt = document.createElement("option")
            opt.setAttribute("value", "")
            opt.setAttribute("selected","")
            opt.setAttribute("disabled","")
            opt.setAttribute("hidden","")
            opt.innerHTML="Veuillez Choisir"
            select.appendChild(opt)
            for (prod of data) {
                var option = document.createElement("option")
                option.innerHTML = prod[0]
                option.setAttribute("value",prod[1])
                select.appendChild(option);
            }
            target.appendChild(elt)
            target.appendChild(select)
    
          })
        })
    
}


recommended_products = []

function get_recommandation() {
  console.log("Dans le panier:",selected_products)

  fetch('http://127.0.0.1:5000/send_recommandation', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(selected_products),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    }).then(function (response) {

      if (response.status !== 200) {
          console.log("Erreur ! Response status: " + response.status);
          return ;
        }
        response.json().then(function(data) {

          console.log("Data reçues :",data);

          recommended_products = data;

          var target = document.getElementById("display_recommandation")
          while (target.firstChild) {
            target.removeChild(target.lastChild);
          }
          var alert = document.createElement("div")
          alert.id = "recommandation"
          alert.classList.add("alert","alert-success")
          alert.setAttribute("value",0)
          alert.innerText = recommended_products[0]
          alert.classList.add("font-weight-bold")
          var icon_add = document.createElement("i")
          icon_add.classList.add("fas","fa-cart-plus","fa-2x","pl-5")
          icon_add.onclick = from_reco_to_list
          icon_add.style.cursor = "pointer"
          alert.appendChild(icon_add)
          target.appendChild(alert)
          var icon = document.createElement("i")
          icon.classList.add("fas","fa-recycle","fa-2x")
          icon.style.cursor = "pointer"
          icon.onclick = change_recommandation
          target.appendChild(icon)

        })
      })
}

function change_recommandation(){
  var alert = document.getElementById("recommandation")
  var alert_value = parseInt(alert.getAttribute("value"))
  if(alert_value < (recommended_products.length - 1)) {

    alert_value += 1
    alert.setAttribute("value",alert_value)
    alert.innerText = recommended_products[alert_value]
    var icon_add = document.createElement("i")
    icon_add.classList.add("fas","fa-cart-plus","fa-2x","pl-5")
    icon_add.onclick = from_reco_to_list
    icon_add.style.cursor = "pointer"
    alert.appendChild(icon_add)
  }
  
}

function from_reco_to_list(){
  var alert = document.getElementById("recommandation")
  li = document.createElement("li")
  li.classList.add("bg-primary","rounded-pill","text-white","m-1","pl-3","pr-3", "d-inline-block")
  li.innerHTML = alert.innerText
  target = document.getElementById("selected_prod")
  target.appendChild(li)

  // On active si necessaire le bouton pour effacer la liste
  var delete_list_btn = document.getElementById("delete_list_btn")
  delete_list_btn.disabled = false;

  // Si plus de trois produits dans le "panier" on peux activer le bouton recommandation
  if(selected_products.length>=3) {
    var reco_btn = document.getElementById("recommandation_btn")
    reco_btn.disabled = false
  }
  change_recommandation()
}