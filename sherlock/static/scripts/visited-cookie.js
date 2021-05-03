function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    var user=getCookie("username");

    // If cookie exists
    if (user != "") {
        alert("Welcome back");
        // "Get Started" directs to node map
        var button = document.querySelector("main__btn");
        button.getAttribute("href");
        button.setAttribute("href", "/node-map");
    }
    // Else generate new cookie
    else {
        alert("New here? Take the tutorial!");
        // "Get Started" directs to tutorial page
        var button = document.querySelector("main__btn");
        button.getAttribute("href");
        button.setAttribute("href", "/splash-page");
    }
}

function tutorialCompleted() {
    user="Completed SherLOCK Tutorial";
    setCookie("username", user, 30);
}