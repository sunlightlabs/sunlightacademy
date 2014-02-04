if (!window.console) {
    window.console = {
        log: function() {}
    };
}

$(document).ready(function() {

    var $subscribeForm = $('form#subscribe');

    $subscribeForm.submit(function(ev) {

        var action = $subscribeForm.attr('action');

        var params = {
            csrfmiddlewaretoken: $subscribeForm.find('input[name=csrfmiddlewaretoken]').val(),
            email: $subscribeForm.find('input[name=email]').val(),
            zipcode: $subscribeForm.find('input[name=zipcode]').val()
        };

        $.post(action, params)
            .success(function(data) {
                $subscribeForm.slideUp();
                $('.subscribe-thanks')
                    .slideDown()
                    .find('p')
                    .text(data.message);
            });

        ev.preventDefault();

    });

});


var asyncload = function(s, id, src) {
    var js, fjs = document.getElementsByTagName(s)[0];
    if (document.getElementById(id)) return;
    js = document.createElement(s); js.id = id; js.src = src;
    fjs.parentNode.insertBefore(js, fjs);
};

var loadFacebook = function() {
    asyncload('script', 'facebook-jssdk',
        '//connect.facebook.net/en_US/all.js#xfbml=1&appId=398451833552688');
};

var loadTwitter = function() {
    asyncload('script', 'twitter-wjs',
        '//platform.twitter.com/widgets.js');
};

var loadLinkedIn = function() {
    asyncload('script', 'linkedin-js',
        '//platform.linkedin.com/in.js');
};
