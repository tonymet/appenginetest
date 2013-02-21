Borrowed = function(){};
Borrowed.prototype.friendsList = function(id){
	var choicesSelect = document.getElementById(id);
	FB.getLoginStatus(function(response) {
		if (response.status == 'not_authorized') {
			alert('you are not authorized');
			return;
		}
		else if(response.status = 'connected'){
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
			});
		}
		else{
			alert('unknown error');
		}
	});
}

function SetCookie(cookieName,cookieValue,nDays) {
	 var today = new Date();
	 var expire = new Date();
	 if (nDays==null || nDays==0) nDays=1;
	 expire.setTime(today.getTime() + 3600000*24*nDays);
	 document.cookie = cookieName+"="+escape(cookieValue)
					 + ";expires="+expire.toGMTString();
}

