Array.prototype.chunk = function(size) {
	let result = [];
	while(this.length) {
		result.push(this.splice(0, size));
	}

	return result;
};

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function murderTheChildren(client) {
	removeAllChildNodes(client);
}

// window.columnPosition = 1;
function populateResults(results, columns=10000) {
	splitResults = results.chunk(columns);
	resultsElement = document.getElementById("results");
	murderTheChildren(resultsElement);

	splitResults.forEach(function(results) {
		rowElement = document.createElement("div");
		rowElement.setAttribute("class", "row d-flex justify-content-center");
		resultsElement.appendChild(rowElement);
		console.log("New row!");

		results.forEach(function(result) {
			console.log("New clolumn!");
			cardElement = document.createElement("div");
			// lineBreakElement = document.createElement("br");
			resultYearElement = document.createElement("p");
			resultTitleElement = document.createElement("p");

			cardElement.setAttribute("class", "card col col-md-2");
			cardElement.setAttribute("style", "background-color: rgba(0, 0, 0, 0.1)");

			resultPosterElement = document.createElement("img");
			resultPosterElement.setAttribute("src", result.poster_url);
			resultPosterElement.setAttribute("class", "result mx-auto d-block rounded");
			resultPosterElement.setAttribute("onclick", "onItemClick("+ JSON.stringify(result) +");");

			anchorElement = document.createElement("a");
			anchorElement.setAttribute("id", "anchor");

			// resultTitleElement.innerText = result.title +"\n("+ result.data.release_year +")";
			resultTitleElement.innerText = result.title;
			resultTitleElement.setAttribute("class", "card-text");

			resultYearElement.innerText = "("+ result.data.release_year +")";
			resultYearElement.setAttribute("class", "card-text text-center");

			rowElement.appendChild(cardElement);
			cardElement.appendChild(anchorElement);
			cardElement.appendChild(resultTitleElement);
			// cardElement.appendChild(lineBreakElement);
			cardElement.appendChild(resultYearElement);
			anchorElement.appendChild(resultPosterElement);
		});
	});
}

async function onItemClick(result) {
	console.log("Sending POST request for "+ result.title);
	search_term = result.url;
	const response = await fetch("http://127.0.0.1:8081/plex?search_term="+ search_term, {
		method: "POST"
	});

	const http_result = await response.json();
	console.log(http_result);
	alert(http_result.message[0]);
	// window.open(http_result.message[0], "_blank");
}

var formElement = document.getElementById("form-id");
formElement.addEventListener("submit", async function(e) {
	loadingWheel = document.createElement("div");
	loadingWheel.setAttribute("class", "preloader");
	formElement.appendChild(loadingWheel);
	e.preventDefault();
	search_term = document.getElementById("search-term-id").value;
	// console.log(search_term);
	const response = await fetch("http://127.0.0.1:8081/plex?search_term="+ search_term, {
		method: "GET"
	});

	const http_result = await response.json();
	loadingWheel.remove();
	console.log(http_result);
	populateResults(http_result.message);
});
