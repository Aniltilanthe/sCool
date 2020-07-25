if (!window.dash_clientside) {
    window.dash_clientside = {};
}

const baseHref = "/home/dataset/";

// create the "ui" namespace within dash_clientside
window.dash_clientside.ui = {
    // this function can be called by the python library
    jsFunction: function(elmntId) {
        console.log(elmntId)
        console.log('Hello Anil . How do you do !')			
		try  {
			//setTimeout(function(){ 
				//var menuInput = document.getElementById('menu-sub-link-input');		
				//console.log(menuInput.value)
				if (elmntId) {
					var scrollToElmnt = document.getElementById(elmntId);
					scrollToElmnt.scrollIntoView();			
				} else {
					window.scrollTo(0,0);
				}
			//}, 50);
		}
		catch (err) {
			console.log('Error scrollIntoView_Menu : ' + err);
		}
    
    }
}


function pageMenuScroll(evt, elmntId) {
	debugger;
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