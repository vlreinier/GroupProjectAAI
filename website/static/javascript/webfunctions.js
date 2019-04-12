// functie voor het opvragen van winkelwagen localstorage producten
function loadProductsShoppingcart() {
	let values = allStorage();
	emptyTable('savedproducts');
	emptyTable('products');
    fetch('/shoppingcart', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(values) })
        .then(response => response.json())
        .then(products_json => showCartInTable(products_json));
    fetch('/collaborativefiltering', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(values) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json,'products'));
}

// functie voor het opvragen van specifieke producten
function loadSelectedProductsPage() {
	let data = {product_for_similar : sessionStorage.getItem('product_for_similar')};
	emptyTable('selectedproduct');
    fetch('/selected', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json, 'selectedproduct'));
    fetch('/selectedsimilar', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json, 'products'));
}

function getProductsOnName() {
	let name = document.forms['productname'].name.value;
	emptyTable('products');
	showProductName(name);
	let selected = 'product'+ document.getElementById("nameorid").value;
	let data = {[selected]: name};
    fetch('/searchedproduct', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json, 'products'));
}

// functie voor het opvragen van persoonlijke producten a.d.h.v. bezoekersid
function loadPersonalPopularProducts(fetchpath) {
    let sessionData = { visitor_id : showVisitorId()};
	emptyTable('products');
    fetch('/'+fetchpath, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(sessionData) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json, 'products'));
}

// functie voor het opvragen van persoonlijke producten a.d.h.v. bezoekersid
function loadPersonalProducts() {
	let visitor_id = sessionStorage.getItem('visitor_id');
	if (visitor_id !== null) {
		document.getElementById("showvisitorid").innerHTML = visitor_id; }
    let sessionData = { visitor_id : sessionStorage.getItem('visitor_id')};
	emptyTable('products');
    fetch('/personalproducts', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(sessionData) })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json, 'products'));
}

// functie voor laden van productdetails in tabel
function showProductsInTable(products, tableid) {
    for (product of products) {
        let row = element("tr",
			element("td", image(product['image'])),
            element("td", text(product['name'])),
			element("td", text(product['price'])),
			element("td", text(product['availability'])),
			element("td", addtostorage_button(product['_id'], product['name'])));
        row.setAttribute('onClick', "addSessionStorage("+product['_id']+");window.location = 'similar.html';");
        document.querySelector("#"+tableid).appendChild(row); }
}

// functie voor laden van productdetails in tabel
function showCartInTable(products) {
    for (product of products) {
        let row = element("tr",
            element("td", text(product['name'])),
            element("td", text(product['price'])),
            element("td", removefromstorage_button(product['_id'])));
        document.querySelector("#savedproducts").appendChild(row); }
}

// functie voor het aanmaken van tabelelementen
function element(name, ...childs) {
    let element = document.createElement(name);
    for (let i=0; i < childs.length; i++) {
        element.appendChild(childs[i]); }
    return element;
}

// functie voor het aanmaken van een textelement voor tabel
function text(value) {
    return document.createTextNode(value);
}

// functie voor het aanmaken van een textelement voor tabel
function image(src) {
    let img = new Image();
	img.src = src;
	img.style.height = '150px';
	img.style.width = '150px';
    return img;
}


// functie voor het aanmaken van een buttonelement voor tabel add to localstorage
function addtostorage_button(id, name) {
	let button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('value', 'Winkelwagen 🛒');
	button.style.fontSize = '20px';
	button.setAttribute('onClick', "addtolocalstorage("+JSON.stringify(id)+','+JSON.stringify(name)+");loadProductsShoppingcart();");
	return button;
}

// functie voor het aanmaken van een buttonelement voor tabel remove from localstorage
function removefromstorage_button(id) {
	let button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('value', 'verwijder');
	button.style.fontSize = '20px';
	button.setAttribute('onClick',"removefromlocalstorage("+JSON.stringify(id)+");loadProductsShoppingcart();");
	return button;
}

// updaten winkelwagentje inhoud hoeveelheid
function updateCartStatus() {
	var length = '('+ localStorage.length +')';
	if (localStorage.length === 0) {
		var length = '';
	}
	document.getElementById("cartbutton").innerHTML = 'Winkelwagentje' + length
}

// functie voor het toevoegen aan LocalStorage
function addtolocalstorage(id, name) {
	localStorage.setItem(id, name);
	event.stopPropagation();
}

// functie voor het verwijderen van een product uit localstorage
function removefromlocalstorage(id) {
	localStorage.removeItem(id);
}

function addSessionStorage(id){
	sessionStorage.removeItem('product_for_similar');
	sessionStorage.setItem('product_for_similar', id);
}

// functie voor het toevoegen aan LocalStorage
function saveVisitorId() {
	let id = document.forms['visitorid']._id.value;
	sessionStorage.clear();
	sessionStorage.setItem('visitor_id', id);
	showVisitorId();
}

function showVisitorId() {
	visitor_id = sessionStorage.getItem('visitor_id');
	if (visitor_id !== null) {
		document.getElementById("showvisitorid").innerHTML = sessionStorage.getItem('visitor_id');
		document.getElementById("popprod").innerHTML ="Producten speciaal voor jou!"; }
	if (visitor_id === "") {
		document.getElementById("popprod").innerHTML ="Populaire producten";}
	return sessionStorage.getItem('visitor_id');
}

function showProductName(name) {
	document.getElementById("popprod").innerHTML = 'Zoekresultaten voor '+ name;
}

// haalt alle waardes uit LocalStorage en slaat deze op in een dictionary
function allStorage() {
	let values = {};
	for (let i = 0; i <= localStorage.length; i++) {
		if (localStorage.key(i) === null) {
			continue; }
		values[localStorage.key(i)] = localStorage.getItem(localStorage.key(i)) }
	return values;
}

// gooit tabel met tableid leeg
function emptyTable(tableid){
	let tableRef = document.getElementById(tableid);
	while (tableRef.rows.length > 1 ) {
		tableRef.deleteRow(1); }
}