if (!window.dash_clientside) {
    window.dash_clientside = {};
}

const baseHref = "/home/dataset/";

// create the "ui" namespace within dash_clientside
window.dash_clientside.ui = {
    // this function can be called by the python library
    jsFunction: function(elmntId) {	
		try  {
			if (elmntId) {
				var scrollToElmnt = document.getElementById(elmntId);
				scrollToElmnt.scrollIntoView();			
			} else {
				window.scrollTo(0,0);
			}
		}
		catch (err) {
			console.log('Error scrollIntoView_Menu : ' + err);
		}    
    },
	
	updateThemeColor : function(newThemeColor) {
		console.log('updateTheme Color');
		console.log('newThemeColor', newThemeColor);
		var bodyStyles = document.body.style;
		bodyStyles.setProperty('--theme-color', newThemeColor);
	}
	
}


function pageMenuScroll(evt, elmntId) {
	console.log('pageMenuScroll evt ', evt);
	console.log('pageMenuScroll elmntId ', elmntId);
	evt = evt || window.event;
	 // stops the default-action from happening
    // means you need to find another way to fire it, if you want to later
    
	if (elmntId) {
		var scrollToElmnt = document.getElementById(elmntId);
		scrollToElmnt.scrollIntoView();	
	}
}