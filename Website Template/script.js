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
		rowElement.setAttribute("class", "row justify-content-center");
		resultsElement.appendChild(rowElement);

		results.forEach(function(result) {
			var cardElement = document.createElement("div");
			var resultYearElement = document.createElement("p");
			var resultTitleElement = document.createElement("p");

			cardElement.setAttribute("class", "card col col-md-2 flex");
			cardElement.setAttribute("style", "background-color: rgba(0, 0, 0, 0.1); animation: swing-in-top-bck 0.6s cubic-bezier(0.175, 0.885, 0.320, 1.275) "+ parseInt(result.data.key)/20 +"s both;");

			resultPosterElement = document.createElement("img");
			resultPosterElement.setAttribute("id", result.data.key);
			resultPosterElement.setAttribute("src", result.poster_url);
			resultPosterElement.setAttribute("class", "result mx-auto d-block rounded");
			resultPosterElement.setAttribute("onclick", "onItemClick("+ JSON.stringify(result) +","+ resultPosterElement.id +");");

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

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
};

async function onItemClick(result, id) {
	console.log(id);
	spinnerContainer = document.createElement("div");
	spinnerContainer.setAttribute("class", "spinner-container masked");
	spinner = document.createElement("img");
	spinner.setAttribute("src", "spinner.svg");
	spinner.setAttribute("class", "spinner");
	spinner.setAttribute("style", "animation: swirl-in-fwd 0.6s ease-out both;");
	// backdrop-filter: blur(6px);
	childElement = document.getElementById(id);
	parentElement = childElement.parentElement;

	parentElement.appendChild(spinnerContainer);
	// spinnerContainer.appendChild(parentElement);
	childElement.setAttribute("style", "filter: blur(2px); cursor: wait;");
	childElement.setAttribute("onclick", "");
	spinnerContainer.setAttribute("style", "cursor: wait;");
	spinnerContainer.appendChild(spinner);

	console.log("Sending POST request for "+ result.title);
	// console.log(JSON.stringify(result));
	search_term = result.url;
	const response = await fetch(
		"http://127.0.0.1:8081/plex?search_term="+ search_term +"&result_data="+ JSON.stringify(result), {
		method: "POST"
	});

	const http_result = await response.json();
	spinner.setAttribute("style", "animation: swirl-out-bck 0.6s ease-in both;");
	childElement.setAttribute("style", "filter: blur(2px); cursor: initial;");
	spinnerContainer.setAttribute("style", "cursor: initial;");
	await sleep(600);
	spinner.setAttribute("src", "check.svg");
	spinner.setAttribute("style", "animation: heartbeat 1.5s ease-in-out both;");
	console.log(http_result);
	// alert(http_result.message);
	// window.open(http_result.message[0], "_blank");
}

var formElement = document.getElementById("form-id");
var formButtomElement = document.getElementById("submit-button-id");
formElement.addEventListener("submit", async function(e) {
	formButtomElement.setAttribute("style", "animation: pulsate-fwd 0.5s ease-in-out both;");
	loadingWheel = document.createElement("div");
	loadingWheel.setAttribute("class", "preloader");
	document.body.appendChild(loadingWheel);
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
	formButtomElement.setAttribute("style", "");
});
