selected_products = []

function choose_prod(){
  var sel = document.getElementById("select_prod");
  var prod_txt = sel.options[sel.selectedIndex].text;
  // var prod_id = sel.value;
  li = document.createElement("li")
  li.innerHTML = prod_txt
  target = document.getElementById("selected_prod")
  target.appendChild(li)
  // On ajoute également l'id du produit dans un array pour faire notre requete recomamndation
  selected_products.push(prod_txt)
}

function delete_liste_prod() {
  // Si user efface la liste on efface les elements du dom et on vide notre array
  target = document.getElementById("selected_prod")
  while (target.firstChild) {
    target.removeChild(target.lastChild);
  }
  reco = document.getElementById("display_recommandation")
  while (reco.firstChild) {
    reco.removeChild(reco.lastChild);
  }
  selected_products = []
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
          alert.innerHTML = recommended_products[0]
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
  var reco= document.getElementById("recommandation")
  var reco_value = parseInt(reco.getAttribute("value"))
  if(reco_value < (recommended_products.length - 1)) {

    reco_value = reco_value + 1
    reco.setAttribute("value",reco_value)
    reco.innerHTML = recommended_products[reco_value]
  }

  console.log(recommended_products[reco_value])
  
}