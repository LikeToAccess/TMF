// function createCorsRequest(method, url) {
// 	var xhr = new XMLHttpRequest();
// 	if ("withCredentials" in xhr) {

// 		// Check if the XMLHttpRequest object has a "withCredentials" property.
// 		// "withCredentials" only exists on XMLHTTPRequest2 objects.
// 		xhr.open(method, url, true);

// 	} else if (typeof XDomainRequest != "undefined") {

// 		// Otherwise, check if XDomainRequest.
// 		// XDomainRequest only exists in IE, and is IE's way of making CORS requests.
// 		xhr = new XDomainRequest();
// 		xhr.open(method, url);

// 	} else {

// 		// Otherwise, CORS is not supported by the browser.
// 		xhr = null;

// 	}
// 	return xhr;
// }

// function makeCorsRequest(url, http_method="GET") {
// 	var xhr = createCorsRequest(http_method, url);
// 	if (!xhr) {
// 		throw new Error("CORS not supported");
// 	}

// 	xhr.onload = function() {
// 		var resultsElement = document.getElementById("results");
// 		var results = JSON.parse(xhr.responseText)["message"];
// 		console.log(results);
// 		results.forEach(function(result) {
// 			lineElement = document.createElement("hr");
// 			resultTitleElement = document.createElement("p");
// 			resultTitleElement.innerText = result["title"];

// 			resultPosterElement = document.createElement("img");
// 			resultPosterElement.setAttribute("src", result["poster_url"]);
// 			// resultPosterElement.setAttribute("width", 150);
// 			resultPosterElement.setAttribute("class", "result");
// 			resultPosterElement.setAttribute("onclick", "alert('Test!');");
// 			// resultPosterElement.setAttribute("style", "cursor: pointer;");

// 			anchorElement = document.createElement("a");
// 			// anchorElement.setAttribute("href", "");
// 			anchorElement.setAttribute("id", "anchor");

// 			resultsElement.appendChild(anchorElement);
// 			resultsElement.appendChild(resultTitleElement);
// 			resultsElement.appendChild(lineElement);
// 			anchorElement.appendChild(resultPosterElement);
// 		});
// 		// resultsElement.innerText = results;
// 		// process the response.
// 	};

// 	xhr.onerror = function() {
// 		console.log("There was an error!");
// 	};

// 	xhr.send();
// }

// function submitForm(formElement) {
// 	var formData = new FormData(formElement);
// 	var search_term = formData.get("search_term");
// 	console.log(search_term);
// 	makeCorsRequest("http://127.0.0.1:8080/plex?search_term="+ search_term);
// }

// var formElement = document.getElementById("form-id");
// document.getElementById("form-submit-id").addEventListener("click", function() {
// 	submitForm(formElement);
// });

function populateResults(results) {
	var resultsElement = document.getElementById("results");

	results.forEach(function(result) {
		lineElement = document.createElement("hr");
		resultTitleElement = document.createElement("p");
		resultTitleElement.innerText = result["title"];

		resultPosterElement = document.createElement("img");
		resultPosterElement.setAttribute("src", result["poster_url"]);
		resultPosterElement.setAttribute("class", "result");
		resultPosterElement.setAttribute("onclick", "alert('Test!');");

		anchorElement = document.createElement("a");
		anchorElement.setAttribute("id", "anchor");

		resultsElement.appendChild(anchorElement);
		resultsElement.appendChild(resultTitleElement);
		resultsElement.appendChild(lineElement);
		anchorElement.appendChild(resultPosterElement);
	});
}

var formElement = document.getElementById("form-id");
formElement.addEventListener("submit", async function(e) {
	e.preventDefault();
	search_term = document.getElementById("search-term-id").value;
	console.log(search_term);
	const response = await fetch("http://127.0.0.1:8080/plex?search_term="+ search_term, {
		method: "GET"
		// headers: { "Content-Type": "application/json" },
		// body: JSON.stringify(Object.fromEntries(formData))
	});

	const result = await response.json();
	console.log(result);
	populateResults(result["message"]);
});
