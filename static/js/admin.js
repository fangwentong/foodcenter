/*sidebar > collapse*/
!function ($) {
    $(document).on("click","ul.nav li.parent > a > span.icon", function(){
        $(this).find('em:first').toggleClass("fa-minus");
    });
    $(".sidebar span.icon").find('em:first').addClass("fa-plus");
}(window.jQuery);

if ($(window).width() > 768) {
	$('#sidebar-collapse').collapse('show');
}
else if ($(window).width() <= 768) {
	$('#sidebar-collapse').collapse('hide');
}
