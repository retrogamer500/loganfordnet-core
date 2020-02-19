function toggleMenu() {
    $('.menu').toggleClass('stowed');
    $('.dimmer').toggleClass('dimmed');
    $('.hamburger-menu').toggleClass('clicked');
}

$(document).ready(function() {
    $('.hamburger-menu').click(function(){
        toggleMenu();
    });
    
    $('.dimmer').click(function(){
        if($('.dimmer').css('opacity') > .1) {
            toggleMenu();
        }
    });
});
