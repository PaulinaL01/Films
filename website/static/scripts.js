function loadContent() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
            document.getElementById("movies").innerHTML = this.responseText;
		}
	};
	xhttp.open('GET', '/api/popular/8', true);
	xhttp.send();
}