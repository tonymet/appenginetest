Borrowed = function(){};
Borrowed.prototype.friendsList = function(id){
	var choicesSelect = document.getElementById(id);
	FB.getLoginStatus(function(response) {
		if (!response.session) {
			alert('you are not connected');
			return;
		}
		FB.api('/me/friends' , function(result) {
			var markup = '';
			var numFriends = result.data ? Math.min(5, result.data.length) : 0;
			if (numFriends > 0) {
				for (var i=0; i<numFriends; i++) {
					o = document.createElement('option');
					o.setAttribute('value', result.data[i].id);
					choicesSelect.appendChild(o);
					t = document.createTextNode(result.data[i].name);
					o.appendChild(t);
				}
			}
			profilePicsDiv.innerHTML = markup;
			FB.XFBML.parse(profilePicsDiv);
		});
	});
}

window.addEventListener('load', function(){
		b = new Borrowed();
		b.friendsList('choices_select');
	}, false);
