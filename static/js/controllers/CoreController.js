var app = app || {};
$(function($){
	//Core Controller
	app.CoreController = {
		init: function()
		{
			this.setUpDropDowns()
			this.setUpSearch()
		},
		setUpDropDowns: function()
		{
			
			$(".toggle-nav-drop-down").click(function(){
				if( $("#explore-drop-down").hasClass("blank") ){
					var position = $(".toggle-nav-drop-down").offset();
					var left = position.left-20;
					$("#explore-drop-down").removeClass("blank").addClass("nav-drop-down").css("left",left);
				} else {
					$("#explore-drop-down").removeClass("nav-drop-down").addClass("blank")
				}
		
			})
			$(".toggle-myaccount-drop-down").click(function(){
				if( $("#myaccount-drop-down").hasClass("blank") ){
					var position = $(".toggle-myaccount-drop-down").offset();
					var left = position.left-17;
					$("#myaccount-drop-down").removeClass("blank").addClass("nav-drop-down").css("left",left);
				} else {
					$("#myaccount-drop-down").removeClass("nav-drop-down").addClass("blank")
				}
		
			})
			
		},
		setUpSearch: function()
		{
			thisController = this;
			$("#search").focus(function(){
				$("#tab-group").fadeOut(250);
				$( "#search" ).parent().parent().animate({
				    width: "865px",
				  }, 500, function() {
				  });
	    		$(".search-result-container").removeClass("blank");
			})
			$("#search").blur(function(){	
				setTimeout(function(){
					$( "#search" ).parent().parent().animate({
					    width: "313px",
					  }, 250, function() {
					    $("#tab-group").fadeIn(200);
					  });
	    		  	$(".search-result-container").addClass("blank");
				}, 400)
			})
			$("#search").keyup(function(e){
				if($(e.currentTarget).val().length > 1){
					thisController.searchFormHandler(e);
				}
			})
		},
		searchFormHandler: function(e)
		{
			var frm = $('#search_form');
			$.ajax({
		    	type: frm.attr('method'),
				url: frm.attr('action'),
				data: frm.serialize(),
		        success: function (data) {
					if(data == 400) {
						$("#search_result_list_holder").html("<p class='noResult'>Start typing to begin your search. Search people, career experiences and career topics.</p>");
					} else{
						$("#search_result_list_holder").html(data);	
					}
									
				},
				error: function(data) {
					thisController.misc.headerAlert("Something went wrong! Please refresh the page and try again.","error",15000);					
		        }
			});
		}
		
	}
});