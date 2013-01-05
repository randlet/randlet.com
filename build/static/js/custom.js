/* Slider */

$(function() {
	$('#da-slider').cslider({
		autoplay	: true,
		interval : 9000
	});
			
});

/* Slide up & Down */

$(".discover a").click(function(e){
	e.preventDefault();
	var myClass=$(this).attr("id");
	$(".dis-content ."+myClass).toggle('slow');
});


/* Image slideshow */

$('#s1').cycle({ 
    fx:    'fade', 
    speed:  1000,
    timeout: 300,
    pause: 1
 });

/* Support */

$("#slist a").click(function(e){
   e.preventDefault();
   $(this).next('p').toggle(200);
});

/* prettyPhoto Gallery */

jQuery("a[class^='prettyPhoto']").prettyPhoto({
overlay_gallery: false, social_tools: false
});


/* Isotype */

// cache container
var $container = $('#portfolio');
// initialize isotope
$container.isotope({
  // options...
});

// filter items when filter link is clicked
$('#filters a').click(function(){
  var selector = $(this).attr('data-filter');
  $container.isotope({ filter: selector });
  return false;
});