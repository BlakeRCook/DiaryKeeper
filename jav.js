// loadPage();
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
	fetch("http://localhost:8080/messages/" + thepost.toString(), {credentials: 'include'}).then(function (response) { 
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
		credentials: 'include',
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
		credentials: 'include',
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
		method:"GET",
		credentials: 'include'
	}).then(function(response){
		console.log("a post was clicked");
		//loadPage();
	});
};


var DelBtn = document.querySelector('#DelBtn');
DelBtn.onclick = function (){
	fetch("http://localhost:8080/messages/" + thepost.toString(), {method: "GET", credentials: 'include'}).then(function (response) { 
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
			credentials: 'include'
		}).then(function (response) {
			console.log("post was deleted")
			var CurrentSelectd = document.querySelector('#CurrentPost');
			CurrentSelectd.innerHTML = fourm.name + "'s post was deleted"
			loadPage();
		});
	}
}


function loadPage(){
	fetch("http://localhost:8080/messages", {credentials: 'include'}).then(function (response) { 
	if (response.status == 200){
		response.json().then(function(fourm) { //waiting for the unpackaged data
		//document.getElementById("textbox").value = "";
		console.log("fourm:", fourm);
		turnoff();
		DisplayFourm(fourm);
	});
	}//wait for server to get us
	else
	{
		//do nothing
	}
}); //part of the response
}


var registerBtn1 = document.querySelector('#re_registerbutton1');
registerBtn1.onclick = function (){
	turnOnRegistration();
}

function turnOnRegistration(){
	document.getElementById("ex_emailbox").style.display = "none";
	document.getElementById("ex_passwordbox").style.display = "none";
	document.getElementById("ex_loginbutton").style.display = "none";
	document.getElementById("re_registerbutton1").style.display = "none";

	document.getElementById("re_registerbutton2").style.display = "inline";
	document.getElementById("re_emailbox").style.display = "inline";
	document.getElementById("re_passwordbox1").style.display = "inline";
	document.getElementById("re_passwordbox2").style.display = "inline";
	document.getElementById("PasswordRetypetxt").style.display = "inline";
	document.getElementById("firstnametxt").style.display = "inline";
	document.getElementById("lastnametxt").style.display = "inline";
	document.getElementById("re_firstnamebox").style.display = "inline";
	document.getElementById("re_lastnamebox").style.display = "inline";
}

var registerBtn2 = document.querySelector('#re_registerbutton2');
registerBtn2.onclick = function (){
	var re_password1 = document.querySelector("#re_passwordbox1");
	var re_password2 = document.querySelector("#re_passwordbox2");
	if(re_password1.value == re_password2.value && re_password1.value != ""){
		
		var re_firstname = document.querySelector("#re_firstnamebox");
		var re_lastname = document.querySelector("#re_lastnamebox");
		var re_email = document.querySelector("#re_emailbox");
		var re_password = document.querySelector("#re_passwordbox1");
		createUser(re_firstname.value, re_lastname.value, re_email.value, re_password.value);

		//confirm("Account Created. you can now login with credentials.")
		toLogin();
	} else{
		confirm("please retype password")
	}
}

function toLogin(){
	document.getElementById("ex_emailbox").style.display = "inline";
	document.getElementById("ex_passwordbox").style.display = "inline";
	document.getElementById("ex_loginbutton").style.display = "inline";
	document.getElementById("re_registerbutton1").style.display = "inline";

	document.getElementById("re_registerbutton2").style.display = "none";
	document.getElementById("re_emailbox").style.display = "none";
	document.getElementById("re_passwordbox1").style.display = "none";
	document.getElementById("re_passwordbox2").style.display = "none";
	document.getElementById("PasswordRetypetxt").style.display = "none";
	document.getElementById("firstnametxt").style.display = "none";
	document.getElementById("lastnametxt").style.display = "none";
	document.getElementById("re_firstnamebox").style.display = "none";
	document.getElementById("re_lastnamebox").style.display = "none";
}

var createUser = function (FirstName, LastName, Email, Password){
	//var someData = "name=" + encodeURIComponent(name); //not supose to be hard coded.
	var data = `firstname=${encodeURIComponent(FirstName)}`;
	data += `&lastname=${encodeURIComponent(LastName)}`;
	data += `&email=${encodeURIComponent(Email)}`;
	data += `&password=${encodeURIComponent(Password)}`;

	fetch("http://localhost:8080/users", {
		//method, body, header
		method: "POST",
		body: data,
		credentials: 'include',
		headers: {
			"Content-type": "application/x-www-form-urlencoded"
		}
	}).then(function(response){ //{} is an js object thats a dictionary.
		if (response.status == 422) {
			alert("User already exists")
			turnOnRegistration();
		}
		else{
			console.log("A User was created");
			confirm("Account Created. you can now login with credentials.")
			loadPage();
		}
	});
};//part of the request

var loginBtn = document.querySelector('#ex_loginbutton');
loginBtn.onclick = function (){
	var email = document.querySelector("#ex_emailbox");
	var password = document.querySelector("#ex_passwordbox");

	var data = `email=${encodeURIComponent(email.value)}`;
	data += `&password=${encodeURIComponent(password.value)}`;

	fetch("http://localhost:8080/sessions", {
		//method, body, header
		method: "POST",
		body: data,
		credentials: 'include',
		headers: {
			"Content-type": "application/x-www-form-urlencoded"
		}
	}).then(function(response){
		if(response.status == 401)
		{
			alert("Email or password is wrong")
			toLogin();
		}
		else
		{
			console.log("A session is starting");
			turnoff();
			loadPage();
		}
	});
}

function turnoff () {
	document.getElementById("loginpromt").style.display = "none";
 	document.getElementById("ex_emailbox").style.display = "none";
	document.getElementById("ex_passwordbox").style.display = "none";
	document.getElementById("ex_loginbutton").style.display = "none";
	document.getElementById("re_registerbutton1").style.display = "none";
	document.getElementById("re_registerbutton2").style.display = "none";
	document.getElementById("re_emailbox").style.display = "none";
	document.getElementById("re_passwordbox1").style.display = "none";
	document.getElementById("re_passwordbox2").style.display = "none";
	document.getElementById("PasswordRetypetxt").style.display = "none";
	document.getElementById("firstnametxt").style.display = "none";
	document.getElementById("lastnametxt").style.display = "none";
	document.getElementById("re_firstnamebox").style.display = "none";
	document.getElementById("re_lastnamebox").style.display = "none";

}
loadPage();
	//have to go to every fetch request for this all the post/get/put/etc.
	//with the (Method, body) all we do is add (credentials: 'include')
	//for fetch requests with no settings at the end
	//"localhost", {credentials: 'include'}).
	//422 failure validation and dup emails