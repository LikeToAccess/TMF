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

const sleep = (milliseconds) => {
	return new Promise(resolve => setTimeout(resolve, milliseconds));
};

function captchaPopUp(src, remainingEpisodeUrls, result, id) {
	// <div class="overlay">
	// 	<div id="captcha-container">
	// 		<p>Captcha!</p>
	// 		<img src="https://gomovies-online.cam/site/captcha" id="captcha-image" style="background:#fff;">
	// 		<form>
	// 			<input type="text" id="captcha-response-id">
	// 			<input type="submit" value="Submit" id="captcha-submit-button-id">
	// 		</form>
	// 	</div>
	// </div>
	var overlayElement = document.createElement("div");
	var captchaContainerElement = document.createElement("div");
	var captchaTitleElement = document.createElement("p");
	var captchaImageElement = document.createElement("img");
	var captchaFormElement = document.createElement("form");
	var captchaResponseElement = document.createElement("input");
	var captchaSubmitButtonElement = document.createElement("input");

	overlayElement.setAttribute("class", "overlay");
	overlayElement.setAttribute("style", "animation: fade-in 0.6s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;");

	captchaContainerElement.setAttribute("id", "captcha-container");
	captchaContainerElement.setAttribute("style", "animation: slide-in-blurred-top 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;");

	captchaTitleElement.innerText = "Captcha!";

	captchaImageElement.setAttribute("src", src);
	captchaImageElement.setAttribute("id", "captcha-image");

	captchaResponseElement.setAttribute("type", "text");
	captchaResponseElement.setAttribute("id", "captcha-response-id");

	captchaSubmitButtonElement.setAttribute("type", "submit");
	captchaSubmitButtonElement.setAttribute("value", "Submit");
	captchaSubmitButtonElement.setAttribute("id", "captcha-submit-button-id");

	document.body.appendChild(overlayElement);
	overlayElement.appendChild(captchaContainerElement);
	captchaContainerElement.appendChild(captchaTitleElement);
	captchaContainerElement.appendChild(captchaImageElement);
	captchaContainerElement.appendChild(captchaFormElement);
	captchaFormElement.appendChild(captchaResponseElement);
	captchaFormElement.appendChild(captchaSubmitButtonElement);

	captchaFormElement.addEventListener("submit", async function(e) {
		captchaSubmitButtonElement.setAttribute("style", "animation: pulsate-fwd 0.5s ease-in-out both;");
		e.preventDefault();
		captchaResponse = captchaResponseElement.value;
		const response = await fetch(`${API_HOST}:${api_port}/captcha?key=${captchaResponse}`, {
			method: "POST",
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
			body: JSON.stringify(
				{
					// "result": {
					// 	"title": result.title,
					// 	"poster_url": result.poster_url,
					// 	"url": result.url,
					// 	"data": result.data
					// }
					"result": result
				}
			)  // Pass through result context as JSON
		}).catch(function() {
			alert("API Error!");
		});

		const raw_response = await response;
		const http_result = await raw_response.json();
		console.log(http_result);
		if (raw_response.status == 200) {
			console.log("Captcha solved!");
			overlayElement.remove();
			if (remainingEpisodeUrls) {
				await finishRemainingEpisodes(result, id, remainingEpisodeUrls);
			} else {
				await onItemClick(result, id);
			}
		} else if (raw_response.status == 225) {
			console.log("Captcha not solved.");
		} else {
			alert("HTTP response status code: "+ raw_response.status +"\n"+ http_result.message);
		}

		await sleep(500);
		captchaSubmitButtonElement.removeAttribute("style");
	});
}

function populateResults(results) {
	resultsElement = document.getElementById("results-section");
	murderTheChildren(resultsElement);

	results.forEach(async function(result) {
		var searchResult = document.createElement("div");
		var resultThumbnail = document.createElement("img");
		var resultTitle = document.createElement("p");
		var resultYear = document.createElement("p");
		var resultImdb = document.createElement("p");
		var resultDuration = document.createElement("p");

		searchResult.setAttribute("class", "search-result");
		// searchResult.setAttribute("width", "200px");
		searchResult.setAttribute("style", "animation: swing-in-top-bck 0.6s cubic-bezier(0.175, 0.885, 0.320, 1.275) "+ parseInt(result.data.key)/20 +"s both;"); // this is causing issues with the hover on searchResult

		resultThumbnail.setAttribute("id", result.data.key);
		resultThumbnail.setAttribute("src", result.poster_url);
		resultThumbnail.setAttribute("class", "result-thumbnail");
		resultThumbnail.setAttribute("onclick", "onItemClick("+ JSON.stringify(result) +","+ resultThumbnail.id +");");

		resultTitle.innerText = result.title;
		resultTitle.setAttribute("class", "result-title");


		// resultYear.innerText = "("+ result.data.release_year +")";
		resultYear.innerText = " "+ result.data.release_year +" ";
		resultYear.setAttribute("class", "result-year label");

		resultImdb.innerText = " "+ result.data.imdb_score +" ";
		resultImdb.setAttribute("class", "result-imdb label");

		resultDuration.innerText = " "+ result.data.duration +" ";
		resultDuration.setAttribute("class", "result-duration label");

		resultsElement.appendChild(searchResult);
		searchResult.appendChild(resultThumbnail);
		searchResult.appendChild(resultTitle);
		searchResult.appendChild(resultYear);
		searchResult.appendChild(resultImdb);
		searchResult.appendChild(resultDuration);

		await sleep(600 + parseInt(result.data.key)/0.02); // this is causing issues with the hover on searchResult
		searchResult.removeAttribute("style");
	});
}

async function finishRemainingEpisodes(result, id, remainingEpisodeUrls) {
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

	resultThumbnail.setAttribute("style", "filter: url(#svg-blur); cursor: url('not-allowed.svg'), not-allowed;");
	resultThumbnail.setAttribute("onclick", "");

	searchResult.appendChild(spinnerContainer);
	console.log("Sending POST request for "+ result.title);

	const response = await fetch(`${API_HOST}:${api_port}/search?query=${query}&data=${JSON.stringify(result)}`, {
		method: "POST",
		headers: {
			"Accept": "application/json",
			"Content-Type": "application/json"
		},
		body: JSON.stringify(
			{
				// "result": {
				// 	"title": result.title,
				// 	"poster_url": result.poster_url,
				// 	"url": result.url,
				// 	"data": result.data
				// }
				"remaining_episode_urls": remainingEpisodeUrls
			}
		)  // Pass through result context as JSON
	}).catch(function() {
		alert("API Error!");
	});
}

async function onItemClick(result, id) {
	console.log(result.data.quality_tag);
	if (result.data.quality_tag == "CAM") {
		var proceed_to_download = confirm(result.title +" is in "+ result.data.quality_tag +" quality. Are you sure you want to proceed?");
		if (!proceed_to_download) {
			return;
		}
	}
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

	resultThumbnail.setAttribute("style", "filter: url(#svg-blur); cursor: url('not-allowed.svg'), not-allowed;");
	resultThumbnail.setAttribute("onclick", "");

	searchResult.appendChild(spinnerContainer);

	console.log("Sending POST request for "+ result.title);
	query = result.url;
	const response = await fetch(
		`${API_HOST}:${api_port}/search?query=${query}&data=${JSON.stringify(result)}`, {
		method: "POST",
		headers: {
			"Accept": "application/json",
			"Content-Type": "application/json"
		},
		body: JSON.stringify(
			{
				"result": null
			}
		)
	});

	const raw_response = await response;
	const http_result = await raw_response.json();

	if (raw_response.status == 225) {
		const captchaImage = http_result.data;
		const remainingEpisodeUrls = http_result.remaining_episode_urls;
		// console.log(captchaImage);
		console.log(http_result);
		stopSpinner(spinner);
		console.log("HTTP response status code: "+ raw_response.status +"\n"+ http_result.message);
		captchaPopUp(captchaImage, remainingEpisodeUrls, result, id);
	} else if (raw_response.status == 201) {
		spinner.setAttribute("style", "animation: swirl-out-bck 0.6s ease-in both;");
		await sleep(600);
		resultThumbnail.setAttribute("style", "filter: url(#svg-blur); cursor: initial;");
		spinnerContainer.removeAttribute("style", "cursor: initial;");
		spinner.setAttribute("src", "check.svg");
		spinner.setAttribute("style", "animation: heartbeat 1.5s ease-in-out both;");
		console.log(http_result);
		console.log(raw_response.status);
		await sleep(1500);
		spinner.removeAttribute("style");
	} else {
		stopSpinner(spinner);
		alert("HTTP response status code: "+ raw_response.status +"\n"+ http_result.message);
	}
}

async function stopSpinner(spinner) {
	spinner.setAttribute("style", "animation: swirl-out-bck 0.6s ease-in both;");
	await sleep(600);
	spinner.setAttribute("src", "error.svg");
	spinner.setAttribute("style", "animation: heartbeat 1.5s ease-in-out both;");
	await sleep(1500);
	spinner.removeAttribute("style");
}

api_port = API_PORT;
var betaToggleElement = document.getElementById("beta-toggle");
betaToggleElement.addEventListener("change", function() {
	if (this.checked) {
		api_port = 8082;
	} else {
		api_port = API_PORT;
	}
});

// var popButtomElement = document.getElementById("pop-button-id");
// popButtomElement.addEventListener("submit", async function(e) {
// 	popButtomElement.setAttribute("style", "animation: pulsate-fwd 0.5s ease-in-out both;");
// 	loadingWheel = document.createElement("div");
// 	loadingWheel.setAttribute("class", "preloader");
// 	document.body.appendChild(loadingWheel);
// 	// e.preventDefault();
// });
var formElement = document.getElementById("input-section");
var formButtomElement = document.getElementById("submit-button-id");
formElement.addEventListener("submit", async function(e) {
	formButtomElement.setAttribute("style", "animation: pulsate-fwd 0.5s ease-in-out both;");
	loadingWheel = document.createElement("div");
	loadingWheel.setAttribute("class", "preloader");
	document.body.appendChild(loadingWheel);
	e.preventDefault();
	query = document.getElementById("search-term-id").value;
	const response = await fetch(`${API_HOST}:${api_port}/search?query=${query}`, {
		method: "GET"
	}).catch(function() {
		alert("API Error!");
	});

	loadingWheel.remove();
	const http_result = await response.json();
	console.log(http_result);
	populateResults(http_result.message);
	formButtomElement.setAttribute("style", "");
});
