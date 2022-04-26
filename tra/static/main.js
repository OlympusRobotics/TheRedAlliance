 
// handler for bulma notification animations
$('.delete').on('click', function() {
    $(this).parent().addClass("animate__backOutLeft");
    $(this).parent().on('animationend', () => {
        $(this).parent().remove();
    });
})
