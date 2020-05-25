function UserMessage(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var col = document.createElement('div');
    col.classList.add("col-9")
    var par = document.createElement('p')
    par.classList.add("d-inline-block","pr-3","pl-3","p-3","rounded-pill","bg-primary","text-white")
    par.innerHTML = content
    col.appendChild(par)
    row.appendChild(col)
    target.append(row)
}

function BotMessage(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var space = document.createElement('div');
    space.classList.add("col-3")
    var col = document.createElement('div');
    col.classList.add("col-9","text-right")
    var par = document.createElement('p')
    par.classList.add("d-inline-block","pr-3","pl-3","p-3","rounded-pill","bg-light")
    par.innerHTML = content
    col.appendChild(par)
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)
}

function BotList(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var space = document.createElement('div');
    space.classList.add("col-3")
    var col = document.createElement('div');
    col.classList.add("col-9","text-right")
    var ul = document.createElement('ul')
    ul.classList.add("d-inline-block","p-4","rounded","bg-light");
    for (msg of content) {
        var element = document.createElement('li');
        element.innerHTML = msg
        ul.appendChild(element)
    };
    col.appendChild(ul)
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)
}

function BotLinksProduits(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var space = document.createElement('div');
    space.classList.add("col-3")
    var col = document.createElement('div');
    col.classList.add("col-9","text-right")
    var ul = document.createElement('ul')
    ul.classList.add("d-inline-block","p-4","rounded","bg-light");
    for (tuple of content) {
        var element = document.createElement('li');
        var a = document.createElement('a');
        a.innerHTML = tuple[0]
        a.href = "#"
        a.setAttribute("value",tuple[1])
        a.setAttribute("product_id",tuple[1])
        a.setAttribute("onclick","get_producteur(this)")
        element.appendChild(a)
        ul.appendChild(element)
    };
    col.appendChild(ul)
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)
}

function BotLinksProducteurs(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var space = document.createElement('div');
    space.classList.add("col-3")
    var col = document.createElement('div');
    col.classList.add("col-9","text-right")
    var ul = document.createElement('ul')
    ul.classList.add("d-inline-block","p-4","rounded","bg-light");
    for (tuple of content) {
        var element = document.createElement('li');
        text = `À ${tuple[1]}: `;
        element.innerHTML = text;
        var a = document.createElement('a');
        a.innerHTML = tuple[0]
        a.href = "#"
        a.setAttribute("value",tuple[2])
        a.setAttribute("producteur_id",tuple[2])
        a.setAttribute("onclick","get_fiche_producteur(this)")
        element.appendChild(a)
        ul.appendChild(element)
    };
    col.appendChild(ul)
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)

    window.scrollTo(0,document.body.scrollHeight)
}

function get_producteur(link) {
    prod_id = link.getAttribute('product_id')
    console.log("ID du produit cliqué: ",prod_id)
    // TODO
    // Si clic affiche la fiche producteur
    fetch('http://127.0.0.1:5000/get_producteurs', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({id:prod_id}),
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
  
        //   console.log(data);
        console.log(data)
        new BotLinksProducteurs(data)


        })
      })
      return false;
}