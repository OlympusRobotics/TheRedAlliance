// handler for bulma notification animations
$('.notification .delete').on('click', function() {
    $(this).parent().addClass("animate__backOutLeft");
    $(this).parent().on('animationend', () => {
        $(this).parent().remove();
    });
})


// Admin setup account code ------------------------
if (window.location.pathname == "/login/admin") {
    console.log("hello")
    var validatePassword = function () {
        if ($("#password").val() != $("#password-confirm").val()) {
            $("#form-feedback").text("Passwords must match"); // display feedback to the user
            $(".button").prop("disabled", "disabled");
        } else {
            $("#form-feedback").text(""); // display feedback to the user
            $(".button").prop("disabled", ""); // enable the submit button
        }
    }
    $("#password-confirm").on("keyup change", validatePassword);
}
//---------------------------------------------------

    
