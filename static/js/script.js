// Création du user pour stocker info localisation, contexte

function submit_entry(){
    // On récupère la question et on la stocke dans un objet
    var question = document.getElementById("question")
    var entry = {
      sender: 'user',
      question: question.value
    };

    // On affiche la question dans l'interface
    new UserMessage(entry.question)

    // On fait notre requete vers Flask
    fetch('http://127.0.0.1:5000/send_message', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(entry),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    // Puis on attend la réponse de Flask
    .then(function (response) {
      
      if (response.status !== 200) {
        console.log("Erreur ! Response status: " + response.status);
        return ;
      }

      // On transforme la reponse en JSON et on l'affiche
      response.json().then(function(data) {

        console.log(data);

        for (elt of data) {

          if (elt.content == 'p'){
            new BotMessage(elt.message)
            
          } else if (elt.content == 'l'){
            new BotList(elt.message)
          }
        }

        // Après affichage quelques traitements pour l'interface utilisateur
        question.value = '';
        question.focus();
        window.scrollTo(0,document.body.scrollHeight);

      })
    })

  }