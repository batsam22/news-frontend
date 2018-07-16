$(document).ready(function(){

$(".dropdown-trigger").dropdown();
        
    alert('ready');
});

var lang="";

var ajaxRequest = new XMLHttpRequest();
function ajaxResponse1() {
    if (ajaxRequest.readyState != 4)
        return;
    else {
        if (ajaxRequest.status == 200) {
            var response= JSON.parse(ajaxRequest.responseText);
            var txt="";
            for(x in response){
                txt += "<li class='tab'> <a href='#' onclick='headline(\""+response[x].chash+"\")'>"+response[x].category+"</a></li>";
            }
            document.getElementById("content").innerHTML = txt;
        }
        else {
            alert("Request failed: " + ajaxRequest.statusText);
            console.log(ajaxRequest.responseText);
        }
    }
}

function news(l) {
    lang=l;
    if (!ajaxRequest) {
        document.getElementById("content").innerHTML = "Request error!";
        return;
    }
    var myURL = "http://localhost:4000/category/"+lang;

    ajaxRequest.onreadystatechange = ajaxResponse1;
    ajaxRequest.open("GET", myURL);
    ajaxRequest.send(null);
}

var ajaxRequest2 = new XMLHttpRequest();
function ajaxResponse2() {
    if (ajaxRequest2.readyState != 4)
        return;
    else {
        if (ajaxRequest2.status == 200) {
            var response= JSON.parse(ajaxRequest2.responseText);
            var txt="";
            for(x in response){

                txt+="<div class='card'>";
                txt+="<div class='card-image waves-effect waves-block waves-light'>";
                txt+="<img class='activator' src='"+response[x].images+"'></div>";
                txt+="<div class='card-content'>";
                txt+="<span class='card-title activator grey-text text-darken-4'>"+response[x].title+"</span>";
                txt+="<p>"+response[x].description+"</p>";
                txt+="<p>"+response[x].d+"<p>";
                txt+= "<div class='card-reveal'>";
                txt+="<span class='card-title grey-text text-darken-4'>"+response[x].title+"<i class='material-icons right'>close</i></span>";
                txt+="<p>"+response[x].description+"</p>";
                txt+="<a href='"+response[x].url+"'>Read full story here</a>"
                txt+="</div></div></div>";

            }
            document.getElementById("news").innerHTML = txt;
        }
        else {
            alert("Request failed: " + ajaxRequest2.statusText);
            console.log(ajaxRequest2.responseText);
        }
    }
}

function headline(chash) {
    var myURL = "http://localhost:4000/headlines/"+lang+"&"+chash;
    ajaxRequest2.onreadystatechange = ajaxResponse2;
    ajaxRequest2.open("GET", myURL);
    ajaxRequest2.send(null);
}

