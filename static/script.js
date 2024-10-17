// static/script.js
document.getElementById("jobForm").addEventListener("submit", function (e) {
	e.preventDefault();

	const formData = new FormData(this);
	const resultsDiv = document.getElementById("results");
	const analysisResult = document.getElementById("analysisResult");

	resultsDiv.classList.add("hidden");
	analysisResult.textContent = "Analyzing jobs...";
	resultsDiv.classList.remove("hidden");

	axios
		.post("/scrape_and_analyze", formData, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		})
		.then(function (response) {
			// Use the HTML content provided by the server
			analysisResult.innerHTML = response.data.analysis_html;
			resultsDiv.classList.remove("hidden");
		})
		.catch(function (error) {
			analysisResult.textContent = "An error occurred: " + (error.response?.data?.error || error.message);
		});
});
