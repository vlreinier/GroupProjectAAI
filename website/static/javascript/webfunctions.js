// functie voor het opvragen van persoonlijk aanbevolen producten d.m.v. collaborativefiltering
function specificFilteringOnProduct(filtering)  {
	var tableRef = document.getElementById('savedproducts');
	while ( tableRef.rows.length > 0 ) {
		tableRef.deleteRow(0);
		}
	showStorageInTable(allStorage(), filtering);
	if (tableRef.rows.length < 1) {
		document.getElementById('contenttext').innerHTML = 'Sla eerst producten op!';
	}
}

// functie voor het opvragen van persoonlijk aanbevolen producten d.m.v. collaborativefiltering
function onloadspecificFilteringOnProduct(id, filtering)  {
	var tableRef = document.getElementById('products');
	while ( tableRef.rows.length > 1 ) {
		tableRef.deleteRow(1);
		}
	id_dict = {}
	id_dict[id] = id
    fetch('/'+filtering, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(id_dict) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

// functie voor het opvragen van persoonlijke producten a.d.h.v. bezoekersid
function loadPersonalProducts() {
	var tableRef = document.getElementById('products');
	while ( tableRef.rows.length > 1 ) {
		tableRef.deleteRow(1);
		}
    sessionData = {
        _id : document.forms['session']._id.value
    }

    fetch('/personalproducts', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(sessionData) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

// functie voor het opvragen van specifieke producten
function loadPopularProducts() {
	var tableRef = document.getElementById('products');
	while ( tableRef.rows.length > 1 ) {
		tableRef.deleteRow(1);
		}
    fetch('/popularproducts')
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
	}

// functie voor laden van productdetails in tabel
function showProductsInTable(products) {
    for (product of products) {
        var row = element("tr",
            element("td", text(product['name'])),
			element("td", text(product['price'])),
            element("td", text(product['brand'])),
			element("td", text(product['category'])),
			element("td", text(product['availability'])),
			element("td", addtostorage_button(product['_id'], product['name']))
        )
        document.querySelector("#products").appendChild(row);
    }
}

// functie voor laden van localstorage in tabel met button
function showStorageInTable(products, filtering) {
    for (product in products) {
        var row = element("tr",
			element("td", showstorage_button(product, products[product], filtering))
        )
        document.querySelector("#savedproducts").appendChild(row);
    }
}
// functie voor het aanmaken van tabelelementen
function element(name, ...childs) {
    var element = document.createElement(name);
    for (let i=0; i < childs.length; i++) {
        element.appendChild(childs[i]);
    }
    return element;
}

// functie voor het aanmaken van een textelement voor tabel
function text(value) {
    return document.createTextNode(value)
}

// functie voor het aanmaken van een buttonelement voor tabel show local storage for content filtering
function showstorage_button(id, value, filtering) {
	var button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('value', value);
	button.style.width = '600px';
	button.style.background = '#4CAF50';
	button.style.color = 'white';
	button.setAttribute('onClick', "onloadspecificFilteringOnProduct("+JSON.stringify(id)+','+JSON.stringify(filtering)+");");
	return button
}

// functie voor het aanmaken van een buttonelement voor tabel add to localstorage
function addtostorage_button(id, name) {
	var button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('value', 'Sla op');
	button.setAttribute('onClick', "addtolocalstorage("+JSON.stringify(id)+','+JSON.stringify(name)+");");
	return button
}

// functie om een link element te maken
function link(href, value) {
    var link = document.createElement("a");
    link.appendChild(text(value));
    link.setAttribute("href", href);
    link.setAttribute("target", "blank");
    return link;
}

// functie voor het toevoegen aan LocalStorage
function addtolocalstorage(id, name) {
	localStorage.setItem(id, name);
}

// functie voor het leeggooien LocalStorage
function clearlocalstorage() {
	localStorage.clear()
	document.getElementById("localstorage").innerHTML = '';
}

// functie voor het weergeven van inhoud LocalStorage op HTML pagina's
function showlocalstorage() {
	document.getElementById("localstorage").innerHTML = ''
	values = allStorage()
	lijst = '| '
	for (i in values) {
		lijst+=(values[i]+' | ')
	}
	if (lijst.length > 2) {
		document.getElementById("localstorage").innerHTML = lijst;
	}
}

// haalt alle waardes uit LocalStorage en slaat deze op in een dictionary
function allStorage() {
	var values = {};
	for (var i=0; i <= localStorage.length; i++) {
		if (localStorage.key(i) === null) { continue; }
		values[localStorage.key(i)] = localStorage.getItem(localStorage.key(i))
	}
    return values;
}