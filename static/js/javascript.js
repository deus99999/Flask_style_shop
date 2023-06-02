	let favoriteCheck = document.getElementById("favorite_check");
	let favoriteIcon = document.getElementById("favorite_icon");
	let myButton = document.getElementById("myButton");

	myButton.addEventListener("click", function() {
  		if (favoriteCheck.checked) {
    		favoriteCheck.checked = false;
  		} else {
    		favoriteCheck.checked = true;
  		}
	});

	function ChangeFavoriteCheck() {
		if (favoriteCheck.checked) {
			favoriteIcon.style.color = "currentColor";
			favoriteIcon.style.width = "16";
			favoriteIcon.style.height = "16";
		} else {
			favoriteIcon.style.color = "red";
			favoriteIcon.style.width = "18";
			favoriteIcon.style.height = "18";
		}
	}