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

	function ChangeFavoriteCheck(product_id) {
		if (favoriteCheck.checked) {
			favoriteIcon.style.color = "currentColor";
			favoriteIcon.style.width = "16";
			favoriteIcon.style.height = "16";
		} else {
			favoriteIcon.style.color = "red";
			favoriteIcon.style.width = "17";
			favoriteIcon.style.height = "17";
			AddToFavorite(product_id);
		}
	}



	function AddToFavorite(product_id) {
		let xhr = new XMLHttpRequest();
		xhr.open('GET', `/add_to_favorite/${product_id}`);
		xhr.onload = function() {
			if (xhr.status === 200) {
				console.log(xhr.responseText);
			}
		}
		xhr.send();
	}