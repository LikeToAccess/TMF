function populateResults(results) {
	var resultsElement = document.getElementById("results");

	results.forEach(function(result) {
		lineElement = document.createElement("hr");
		resultTitleElement = document.createElement("p");
		resultTitleElement.innerText = result.title;

		resultPosterElement = document.createElement("img");
		resultPosterElement.setAttribute("src", result.poster_url);
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
	populateResults(result.message);
});
