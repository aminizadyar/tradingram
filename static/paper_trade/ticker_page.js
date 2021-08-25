$(".close_position_button").click(function (event) {
    event.preventDefault();
    console.log(event);
    console.log($(this));
    console.log($(this).parent('form').attr('id'));
});