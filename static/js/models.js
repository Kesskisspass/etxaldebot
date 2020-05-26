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
    var ul = document.createElement('ul');
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

    window.scrollTo(0,document.body.scrollHeight)
}

function BotLinksProduits(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var space = document.createElement('div');
    space.classList.add("col-3")
    var col = document.createElement('div');
    col.classList.add("col-9","text-right")
    var ul = document.createElement('ul');
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
    var ul = document.createElement('ul')
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)

    window.scrollTo(0,document.body.scrollHeight)
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
            text = `${tuple[1]}: `;
            element.innerHTML = text;
            var a = document.createElement('a');
            a.innerHTML = tuple[0]
            a.href = "#"
            a.setAttribute("value",tuple[2])
            a.setAttribute("producteur_id",tuple[2])
            a.setAttribute("onclick","get_fiche_producteur(this)")
            element.appendChild(a)
            ul.appendChild(element)
            window.scrollTo(0,document.body.scrollHeight)
        };
    col.appendChild(ul)
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)
    
    window.scrollTo(0,document.body.scrollHeight)
}

function get_producteur(link) {
    prod_id = link.getAttribute('product_id')
    console.log("ID du produit cliqué: ",prod_id);
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

function get_fiche_producteur(link) {
    producteur_id = link.getAttribute('producteur_id')
    console.log("Producteur ID: ",producteur_id)
    fetch('http://127.0.0.1:5000/get_fiche_producteur', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({id:producteur_id}),
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
            new BotFiche(data);
        })
      })
      return false;
}

function BotFiche(content) {
    var target = document.getElementById("conversation")
    var row = document.createElement('div');
    row.classList.add("row")
    var space = document.createElement('div');
    space.classList.add("col-3")
    var col = document.createElement('div');
    col.classList.add("col-9","text-left")
    var div = document.createElement('div')
    div.classList.add("d-inline-block","pr-3","pl-3","p-3","rounded","bg-light")

    div.innerHTML = content[0][0] + "<br>" + content[0][1] + "<br>"  + content[0][2]+ "<br>" + content[0][3]
        var ul = document.createElement("ul")
        for (prod of content[1]) {
            var li = document.createElement("li")
            li.innerHTML = prod
            ul.appendChild(li)
            div.appendChild(ul)
            window.scrollTo(0,document.body.scrollHeight)
        };
    col.appendChild(div)
    row.appendChild(space)
    row.appendChild(col)
    target.append(row)
    
    window.scrollTo(0,document.body.scrollHeight)
}