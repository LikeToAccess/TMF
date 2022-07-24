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

function murderTheChildren(targetToBeExecutedFullNameAndAddressInformation) {
	removeAllChildNodes(targetToBeExecutedFullNameAndAddressInformation);
}

function captchaPopUp(src) {
	captchaContainerElement = document.createElement("div");
	captchaContainerElement.setAttribute("class", "overlay");
	captchaContainerElement.setAttribute("id", "captcha-container");
	captchaImageElement = document.createElement("img");
	captchaImageElement.setAttribute("src", src);
	captchaImageElement.setAttribute("id", "captcha-image");
	// TODO: Add this but for the Captcha API to submit Captcha responses.
	// <form id="input-section" style="animation: slide-in-blurred-top 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;">
	// 		<input type="text" value="Star Wars Episode" id="search-term-id">
	// 		<input type="submit" value="Submit" id="submit-button-id">
	// 	</form>

	document.body.appendChild(captchaContainerElement);
	captchaContainerElement.appendChild(captchaImageElement);
}

const sleep = (milliseconds) => {
	return new Promise(resolve => setTimeout(resolve, milliseconds));
};

function populateResults(results) {
	resultsElement = document.getElementById("results-section");
	murderTheChildren(resultsElement);

	results.forEach(async function(result) {
		var searchResult = document.createElement("div");
		var resultThumbnail = document.createElement("img");
		var resultTitle = document.createElement("p");
		var resultYear = document.createElement("p");

		searchResult.setAttribute("class", "search-result");
		searchResult.setAttribute("style", "animation: swing-in-top-bck 0.6s cubic-bezier(0.175, 0.885, 0.320, 1.275) "+ parseInt(result.data.key)/20 +"s both;"); // this is causing issues with the hover on searchResult

		resultThumbnail.setAttribute("id", result.data.key);
		resultThumbnail.setAttribute("src", result.poster_url);
		resultThumbnail.setAttribute("class", "result-thumbnail");
		resultThumbnail.setAttribute("onclick", "onItemClick("+ JSON.stringify(result) +","+ resultThumbnail.id +");");

		resultTitle.innerText = result.title;
		resultTitle.setAttribute("class", "result-title");

		resultYear.innerText = "("+ result.data.release_year +")";
		resultYear.setAttribute("class", "result-year");

		resultsElement.appendChild(searchResult);
		searchResult.appendChild(resultThumbnail);
		searchResult.appendChild(resultTitle);
		searchResult.appendChild(resultYear);

		await sleep(600 + parseInt(result.data.key)/0.02); // this is causing issues with the hover on searchResult
		searchResult.removeAttribute("style");
	});
}

async function onItemClick(result, id) {
	var spinnerContainer = document.createElement("div");
	var spinner = document.createElement("img");
	var resultThumbnail = document.getElementById(id);
	var searchResult = resultThumbnail.parentElement;

	spinnerContainer.setAttribute("class", "spinner-container masked");
	spinnerContainer.setAttribute("style", "cursor: url('not-allowed.svg'), not-allowed;");
	spinnerContainer.appendChild(spinner);

	spinner.setAttribute("src", "spinner.svg");
	spinner.setAttribute("class", "spinner");
	spinner.setAttribute("style", "animation: swirl-in-fwd 0.6s ease-out both;");

	resultThumbnail.setAttribute("style", "filter: blur(2px); cursor: url('not-allowed.svg'), not-allowed;");
	resultThumbnail.setAttribute("onclick", "");

	searchResult.appendChild(spinnerContainer);

	console.log("Sending POST request for "+ result.title);
	search_term = result.url;
	const response = await fetch(
		API_BASE_URL +"/plex?search_term="+ search_term +"&result_data="+ JSON.stringify(result), {
		method: "POST"
	});

	const raw_response = await response;
	const http_result = await raw_response.json();

	if (raw_response.status == 225) {
		const captchaImage = http_result.data;
		console.log(captchaImage);
		console.log(http_result);
		alert("HTTP response status code: "+ raw_response.status +"\n"+ http_result.message);
		captchaPopUp(captchaImage);
	} else if (raw_response.status == 201) {
		spinner.setAttribute("style", "animation: swirl-out-bck 0.6s ease-in both;");
		await sleep(600);
		resultThumbnail.setAttribute("style", "filter: blur(2px); cursor: initial;");
		spinnerContainer.removeAttribute("style", "cursor: initial;");
		spinner.setAttribute("src", "check.svg");
		spinner.setAttribute("style", "animation: heartbeat 1.5s ease-in-out both;");
		console.log(http_result);
		console.log(raw_response.status);
		await sleep(1500);
		spinner.removeAttribute("style");
	} else {
		alert("HTTP response status code: "+ raw_response.status +"\n"+ http_result.message);
	}
}

var formElement = document.getElementById("input-section");
var formButtomElement = document.getElementById("submit-button-id");
formElement.addEventListener("submit", async function(e) {
	formButtomElement.setAttribute("style", "animation: pulsate-fwd 0.5s ease-in-out both;");
	loadingWheel = document.createElement("div");
	loadingWheel.setAttribute("class", "preloader");
	document.body.appendChild(loadingWheel);
	e.preventDefault();
	search_term = document.getElementById("search-term-id").value;
	const response = await fetch(API_BASE_URL +"/plex?search_term="+ search_term, {
		method: "GET"
	});

	const http_result = await response.json();
	loadingWheel.remove();
	console.log(http_result);
	populateResults(http_result.message);
	formButtomElement.setAttribute("style", "");
});
