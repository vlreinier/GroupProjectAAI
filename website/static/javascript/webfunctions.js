// functie voor het opvragen van specifieke producten
function loadProductsShoppingcart() {
	var tableRef = document.getElementById('savedproducts');
	while ( tableRef.rows.length > 0 ) {
		tableRef.deleteRow(0);
		}
	values = allStorage()
    fetch('/shoppingcart', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(values) })
        .then(response => response.json())
        .then(products_json => showCartInTable(products_json));
	}

// functie voor laden van productdetails in tabel
function showCartInTable(products) {
    for (product of products) {
        var row = element("tr",
            element("td", text(product['name'])),
            element("td", text(product['brand'])),
            element("td", text(product['price'])),
            element("td", removefromstorage_button(product['_id']))
        )
        document.querySelector("#savedproducts").appendChild(row);
    }
}

// functie voor het aanmaken van een buttonelement voor tabel remove from localstorage
function removefromstorage_button(id) {
	var button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('value', 'verwijder');
	button.style.fontSize = '20px';
	button.setAttribute('onClick', "removefromlocalstorage("+JSON.stringify(id)+");");
	return button
}

// functie voor het verwijderen van een product uit localstorage
function removefromlocalstorage(id) {
	localStorage.removeItem(id);
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
function loadProducts(filtering) {
	var tableRef = document.getElementById('products');
	while ( tableRef.rows.length > 1 ) {
		tableRef.deleteRow(1);
		}
	values = allStorage()
    fetch('/'+filtering, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(values) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
	}

// functie voor laden van productdetails in tabel
function showProductsInTable(products) {
    for (product of products) {
        var row = element("tr",
			element("td", image(product['image'])),
            element("td", text(product['name'])),
			element("td", text(product['price'])),
			element("td", text(product['availability'])),
			element("td", addtostorage_button(product['_id'], product['name']))
        )
        document.querySelector("#products").appendChild(row);
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

// functie voor het aanmaken van een textelement voor tabel
function image(src) {
    var img = new Image();
	img.src = src;
	img.style.height = '120px';
	img.style.width = '120px';
    return img;
}


// functie voor het aanmaken van een buttonelement voor tabel add to localstorage
function addtostorage_button(id, name) {
	var button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('value', '🛒');
	button.style.fontSize = '20px';
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


// haalt alle waardes uit LocalStorage en slaat deze op in een dictionary
function allStorage() {
	var values = {};
	for (var i=0; i <= localStorage.length; i++) {
		if (localStorage.key(i) === null) { continue; }
		values[localStorage.key(i)] = localStorage.getItem(localStorage.key(i))
	}
    return values;
}