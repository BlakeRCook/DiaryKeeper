loadPage();
var thepost = 0
var editMode = false
var deleteMode = false
var button = document.querySelector('#button');
button.onclick = function (){
	var name = document.querySelector("#namebox");
	var age = document.querySelector("#agebox");
	var feild = document.querySelector("#textbox");
	var date = document.querySelector("#datebox");
	var ten = document.querySelector("#tenbox");
	if (editMode == true){
		editFourm(name.value, age.value, feild.value, date.value, ten.value);
		editMode = false;
	}
	else{
		createFourm(name.value, age.value, feild.value, date.value, ten.value);
	}
	//createFourm(name.value, age.value, feild.value, date.value, ten.value);
}

var editBtn = document.querySelector('#EditBtn');
editBtn.onclick = function (){
	editMode = true
	fetch("http://localhost:8080/messages/" + thepost.toString()).then(function (response) { 
	response.json().then(function(feild) {
		//console.log("what is this", feild);
		document.getElementById("namebox").value = feild.name;
		document.getElementById("agebox").value = feild.age;
		document.getElementById("textbox").value = feild.sentence;
		document.getElementById("datebox").value = feild.date;
		document.getElementById("tenbox").value = feild.ten;
		document.getElementById("button").value = "Save Changes";

	});
}); 
}

var editFourm = function(name, age, sentence, date, ten){
	var data = `name=${encodeURIComponent(name)}`;
	data += `&age=${encodeURIComponent(age)}`;
	data += `&sentence=${encodeURIComponent(sentence)}`;
	data += `&date=${encodeURIComponent(date)}`;
	data += `&ten=${encodeURIComponent(ten)}`;

	fetch("http://localhost:8080/messages/" + thepost.toString(), {
		method: "PUT",
		body: data,
		headers: {
			"Content-type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		document.getElementById("namebox").value = "";
		document.getElementById("agebox").value = "";
		document.getElementById("textbox").value = "";
		document.getElementById("datebox").value = "";
		document.getElementById("tenbox").value = ""; 
		loadPage();
	}); 
}

var createFourm = function (name, age, sentence, date, ten){
	//var someData = "name=" + encodeURIComponent(name); //not supose to be hard coded.
	var data = `name=${encodeURIComponent(name)}`;
	data += `&age=${encodeURIComponent(age)}`;
	data += `&sentence=${encodeURIComponent(sentence)}`;
	data += `&date=${encodeURIComponent(date)}`;
	data += `&ten=${encodeURIComponent(ten)}`;

	fetch("http://localhost:8080/messages", {
		//method, body, header
		method: "POST",
		body: data,
		headers: {
			"Content-type": "application/x-www-form-urlencoded"
		}
	}).then(function(response){ //{} is an js object thats a dictionary.
		console.log("A fourm was posted");
		document.getElementById("namebox").value = "";
		document.getElementById("agebox").value = "";
		document.getElementById("textbox").value = "";
		document.getElementById("datebox").value = "";
		document.getElementById("tenbox").value = "";
		loadPage();
	});
};//part of the request

var DisplayFourm = function (fourm) {
	document.getElementById("my-list").innerHTML = "";
	var myList = document.querySelector("#my-list");
	fourm.forEach(function (feild){
		var listItem = document.createElement("li");
		listItem.innerHTML = feild.name + ", Age: "+ feild.age + ", date: "+feild.date + "<br />" + feild.sentence + "<br />" + feild.ten + "/10";
		listItem.onclick = function(){
			fourmSelected(feild);
		}
		myList.appendChild(listItem);
	});
};

var fourmSelected = function (feild){
	var CurrentSelectd = document.querySelector('#CurrentPost');
	CurrentSelectd.innerHTML = feild.name + "'s post is selected"
	thepost = feild.id;
	var url = "http://localhost:8080/messages/" + feild.id.toString();
	fetch(url, {
		method:"GET"
	}).then(function(response){
		console.log("a post was clicked");
	});
};


var DelBtn = document.querySelector('#DelBtn');
DelBtn.onclick = function (){
	fetch("http://localhost:8080/messages/" + thepost.toString()).then(function (response) { 
	response.json().then(function(feild) {
		deleteFourm(feild);
	});
}); 
}

var deleteFourm = function (fourm) {
	if(confirm("You want to delete " + fourm.name + "'s post?")){
		console.log("Deleting post with ID", fourm.id);
		fetch("http://localhost:8080/messages/" + thepost.toString(), {
			method: "DELETE",
		}).then(function (response) {
			console.log("post was deleted")
			var CurrentSelectd = document.querySelector('#CurrentPost');
			CurrentSelectd.innerHTML = fourm.name + "'s post was deleted"
			loadPage();
		});
	}
}


function loadPage(){
	fetch("http://localhost:8080/messages").then(function (response) { //wait for server to get us
	response.json().then(function(fourm) { //waiting for the unpackaged data
		//document.getElementById("textbox").value = "";
		console.log("fourm:", fourm);
		DisplayFourm(fourm);
	});
}); //part of the response
}