// handler for bulma notification animations
$('.notification .delete').on('click', function() {

    $(this).parent().addClass("animate__backOutLeft");
    $(this).parent().on('animationend', () => {
        $(this).parent().remove();
    });
})

// Function to delete a scout when clicking the delete button
function deleteScout(id) {
    $.ajax(`/admin/scout/delete/${id}`, {type : "DELETE"})
    .always(function () {
        location.reload(true);
    });
}

// Admin setup account code ------------------------
if (window.location.pathname == "/login/admin") {
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
    // event handler for disabling the new button
    $(".add-scout-panel input").on('keyup change', function() {
        // check if the inputs have anything in them
        if ($("#new-name").val().length > 0 && $("#new-code").val().length > 0) {
            $("#create-new").prop("disabled", "");
        } else {
            $("#create-new").prop("disabled", "disabled");
        }
    });
    // handler for adding new scout
    $("#create-new").on('click', function() {
        var loadingScoutCard = 
`
<div id="loading-card" class="scout-card loading is-flex is-justify-content-center">
    <div>
        <progress class="progress is-large is-danger" max="100">100%</progress>
    </div>
</div>
`       
        $("#scout-cards .column").prepend(loadingScoutCard);
        
        $(this).toggleClass("is-loading");
        $.post("/admin/scout/new", {
                name : $("#new-name").val(),
                code : $("#new-code").val()
            })
            .always(function () {
                location.reload(true);
            });
    });
}
    
// custom form creation code
if (window.location.pathname == "/admin/createform") {
    var questions = [];
    $("#add-question").on("click", function () {
        $()
    });
}