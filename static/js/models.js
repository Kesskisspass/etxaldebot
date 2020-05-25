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