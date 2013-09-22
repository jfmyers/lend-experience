var app = app || {};
$(function($){
	//AddContributionController
	app.AddContributionController = {
		init: function()
		{
			this.tagSetup();
			this.formHandler();			
			this.misc = app.Misc;
		},
		tagSetup: function()
		{
			var thisController = this;
			
			$("#tag_text").keyup(function(e){
				thisController.tagSearch(e)
			})
			$("#tag_text").click(function(e){
				thisController.showTagSearchBox();
			})
			$("#tag_text").blur(function(e){
				setTimeout(function(){
					$(".tag-search-box").addClass("blank");
					$("#tag_text").val("");
				},200)
				
			})
			
			$("#tag-search-results").on("click",".career-topic-result", function(e) {
				thisController.tagAdd(e)
			});
			$('.tag-edit').on("click", ".removeCareerTag", function(e) {
				thisController.tagRemove(e)
			});
		},
		showTagSearchBox: function(e)
		{
			var position = $("#tag_text").position(),
				top = position.top + 45,
				left = position.left + 13;
			
			$(".tag-search-box").css("top",top).css("left", left).removeClass("blank");
		},
		tagAdd: function(e)
		{
			var selector = $(e.currentTarget),
				value = selector.val(),
				type = selector.attr("data-type");
				
			//assign data to hidden input
			$("#tag").val(value);
			$("#tag_type").val(type);
			
			//add new html to the tag-edit div
			var html = "<span class=\"tag-edit-text\">"+value+"</span><button type=\"submit\" class=\"close removeCareerTag\">×</button>";
			$(".tag-edit").html(html);
			
			//hide search div and show selected_tag div
			$("#search_careers").addClass("blank");
			$("#selected_tag").removeClass("blank");
		},
		tagRemove: function(e)
		{
			var selector = $(e.currentTarget),
				parent = selector.parent(),
				grandparent = parent.parent();
			
			//hide grandparent
			$(grandparent).addClass("blank");
			
			//show search
			$("#search_careers").removeClass("blank");
			
			//show the tag search box
			$("#tag_text").focus()
			this.showTagSearchBox()
		},
		tagSearch: function(e)
		{
			var thisController = this,
				value = $(e.currentTarget).val(),
				frm = $('#tag_search_form');
			
			if(value != "" || value != null){
				e.preventDefault();
				$.ajax({
			    	type: frm.attr('method'),
					url: frm.attr('action'),
					data: frm.serialize(),
			        success: function (data) {
						if(data == 400 ) {
							$("#tag-search-results").empty().html("<p>Begin typing to search existing tags or add a new one.</p>");
						} else {
							$("#tag-search-results").empty().html(data);
							
						}
						
					},
					error: function(data) {
						thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
			        }
				});
			    return false;
			}
		},
		formHandler: function()
		{
			var thisController = this,
			 	frm = $('#add_contribution_form');

			frm.submit(function (e) {
				e.preventDefault();
				// Get description with formatting and place in the formatted text area
				$("#formatted_description").text( $("#editor").html() );
				// Get rid of formatting from description and place in description text area
				$("#description").text( thisController.misc.cleanEditorText() );
				// Display the loader gif.
				$(".saving-form").removeClass("blank");
				// Disable the submit button.
				$("#submit").attr("disabled",true);
				// Submit the form via ajax.
				
				$.ajax({
			    	type: frm.attr('method'),
					url: frm.attr('action'),
					data: frm.serialize(),
			        success: function (data) {
						$(".saving-form").addClass("blank");
						thisController.misc.headerAlert("Your experience has been saved!","success",8000);
						crsf = $('[name="csrfmiddlewaretoken"]').val();
						$.post("/career/categorize",{post_pk: data.post_pk, csrfmiddlewaretoken:crsf}, function(){})
						setTimeout(function(){
							$("#goToPost").attr("action","/contributions/"+data.post_url+"-"+data.post_pk);
							$("#goToPost").submit();
						},500)
					},
					error: function(data) {
						$("#submit").attr("disabled",false);
						$(".saving-form").addClass("blank");
						
						//Display error messages.
						json = $.parseJSON(data.responseText);
						if(json.title != null) {
							thisController.misc.inputBorderAlert("#title");
							thisController.misc.headerAlert("A title for your experience is required!","error",8000);
						} else if(json.description != null) {
							thisController.misc.inputBorderAlert("#editor");
							thisController.misc.headerAlert("A description for your experience is required!","error",8000);
						} else {
							thisController.misc.headerAlert("Something went wrong! Please refresh the page and try again.","error",15000);
						}
			        }
				});
			});	
		}
	}
});