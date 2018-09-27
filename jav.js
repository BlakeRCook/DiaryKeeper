loadPage();
var button = document.querySelector('#button');
button.onclick = function (){
	var field = document.querySelector("#textbox");
	createSentence(field.value);
	loadPage();
}

var createSentence = function (sentence){
	//var someData = "name=" + encodeURIComponent(name); //not supose to be hard coded.
	var someData = `sentence=${encodeURIComponent(sentence)}`;
	fetch("http://localhost:8080/messages", {
		//method, body, header
		method: "POST",
		body: someData,
		headers: {
			"Content-type": "application/x-www-form-urlencoded"
		}
	}).then(function(response){ //{} is an js object thats a dictionary.
		console.log("A sentence was posted");
		//this is where u want to regrab all pandas
	});
};//part of the request

var DisplaySentence = function (paragraph) {
	document.getElementById("my-list").innerHTML = "";
	var myList = document.querySelector("#my-list");
	paragraph.forEach(function (sentence){
		var listItem = document.createElement("li");
		listItem.innerHTML = sentence;
		myList.appendChild(listItem);
	});
};

function loadPage(){
	fetch("http://localhost:8080/messages").then(function (response) { //wait for server to get us
	response.json().then(function(paragraphs) { //waiting for the unpackaged data
		document.getElementById("textbox").value = "";
		console.log("Paragraphs:", paragraphs);
		DisplaySentence(paragraphs);
	});
}); //part of the response
}