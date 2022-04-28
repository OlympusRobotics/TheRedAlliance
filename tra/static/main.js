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
// admin dashboard code -----------------------------
if (window.location.pathname == "/admin") {

    $("section").hide();
// ------ Handlers for switching tabs    
    // Initially show the scouts tab
    $("#scouts-tab").show();    
    $("#dash-tabs div ul li").on('click', function() {
        $(".is-active").toggleClass('is-active');
        $(this).addClass('is-active');
        let tab = $(this).attr('id');
        $("section").hide();
        // make visible the matching section
        $('#' +tab + '-tab').show(); 
    });
    //------- New scout creation code
    $("#create-new").on('click', function() {
        var scoutCard = 
`
<div class="scout-card">
    <span class="name"></span>
</div>
`
        $(this).toggleClass("is-loading")
        location.reload(true);
    });

}
    
