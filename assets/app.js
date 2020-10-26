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
	
	updateThemeColor : function(newThemeBackgroundColor, newThemeColor) {
		var bodyStyles = document.body.style;
		bodyStyles.setProperty('--theme-background-color', newThemeBackgroundColor);
		bodyStyles.setProperty('--theme-color', newThemeColor);
	},
}