selected_prod_id = []

function choose_prod(){
  var sel = document.getElementById("select_prod");
  var prod_txt = sel.options[sel.selectedIndex].text;
  var prod_id = sel.value;
  li = document.createElement("li")
  li.innerHTML = prod_txt
  target = document.getElementById("selected_prod")
  target.appendChild(li)
  // On ajoute également l'id du produit dans un array pour faire notre requete recomamndation
  selected_prod_id.push(prod_id)
}

function delete_liste_prod() {
  // Si user efface la liste on efface les elements du dom et on vide notre array
  target = document.getElementById("selected_prod")
  while (target.firstChild) {
    target.removeChild(target.lastChild);
  }
  selected_prod_id = []
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