/*$(document).ready(function()
    {
        $(".datagrid").tablesorter();
        $('#accordian h3').accordion();
    });*/
    
$(document).ready(function() {
    $(".datagrid").tablesorter();
	//ACCORDION BUTTON ACTION	
	$('div.accordionButton').click(function() {
		$('div.accordionContent').slideUp('normal');	
		$(this).next().slideDown('normal');
	});
 
	//HIDE THE DIVS ON PAGE LOAD	
	$("div.accordionContent").hide();
 
});