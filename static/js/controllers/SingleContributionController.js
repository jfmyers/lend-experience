var app = app || {};
$(function($){
	//SingleContributionController
	app.SingleContributionController = {
		init: function()
		{
			this.commentSetUp();
			this.tagSetup();
			this.commentFormHandler();
			this.misc = app.Misc;
		},
		commentSetUp: function()
		{
			var thisController = this;
			//$('.comment-input-real').wysiwyg();
			$("#fake-comment-input").click(function(){
				$("#fake-comment-input").parent().addClass("blank");
				$("#text").parent().parent().removeClass("blank");
				$("#text").focus();
			})
			$('.remove-item').on("submit", ".comment-remove-form", function(e) {
				thisController.removeCommentHandler(e)
			})
		},
		tagSetup: function()
		{
			var thisController = this;
			
			$(".edit-tag").click(function(){
				if($(".cancel").parent().parent().hasClass("blank")){
					$(".cancel").parent().parent().removeClass("blank");
					$(".edit-tag").parent().addClass("blank");
				}
				
			})
			$(".cancel").click(function(){
				if($(".edit-tag").parent().hasClass("blank")){
					$(".cancel").parent().parent().addClass("blank");
					$(".edit-tag").parent().removeClass("blank");
				}
			})
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
				
			$('#tags-to-remove').on("submit", ".tag_remove_form", function(e) {
				thisController.tagRemove(e)
			});
			
			$('#tag-search-results').on("submit", ".new_tag_form", function(e) {
				thisController.tagAdd(e)
			});
			
		
		},
		showTagSearchBox: function(e)
		{
			var position = $("#tag_text").position(),
				top = position.top + 29,
				left = position.left;
			
			$(".tag-search-box").css("top",top).css("left", left).removeClass("blank");
		},
		tagAdd: function(e)
		{
			e.preventDefault();
			var thisController = this,
				frm = $(e.currentTarget);

			$.ajax({
			    type: frm.attr('method'),
				url: frm.attr('action'),
				data: frm.serialize(),
			    success: function (data) {
					if(data == 400 ) {
						thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
					} else {
						$("#no_tag_alert").remove();
						data = data.split("`");
						$("#current-tags").append(data[0]);
						$("#tags-to-remove").append(data[1]);
						crsf = $('[name="csrfmiddlewaretoken"]').val();
						post_pk = $("#post_pk").val();
						$.post("/career/categorize",{post_pk:post_pk, csrfmiddlewaretoken:crsf}, function(){})
					}	
				},
				error: function(data) {
					thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
			    }
			});
			return false;

		},
		tagRemove: function(e)
		{
			e.preventDefault()
			var thisController = this,
				frm = $(e.currentTarget),
				tag_id = frm.children().first().val(),
				tag_selector = "#tag_"+tag_id;
				
				frm.remove();
				$(tag_selector).remove();
				
			$.ajax({
			    type: frm.attr('method'),
				url: frm.attr('action'),
				data: frm.serialize(),
			    success: function (data) {
					if(data == 400 ) {
						thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
					} else {
						crsf = $('[name="csrfmiddlewaretoken"]').val();
						post_pk = $("#post_pk").val();
						$.post("/career/categorize",{post_pk:post_pk, csrfmiddlewaretoken:crsf}, function(){})
					}
				},
				error: function(data) {
					thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
			    }
			});
			return false;

		},
		tagSearch: function(e)
		{
			thisController = this;
			
			var value = $(e.currentTarget).val();
			var frm = $('#tag_search_form');
			
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
		formFakeStyle: function()
		{
			$("#fake-comment-input").parent().removeClass("blank");
			$("#text").parent().parent().addClass("blank");
			$("#text").val("");
		},
		commentFormHandler: function()
		{
			$(".comment-result").empty()
			
			var thisController = this,
			 	frm = $('#comment-form');
			
			frm.submit(function (e) {
				e.preventDefault();
				$.ajax({
			    	type: frm.attr('method'),
					url: frm.attr('action'),
					data: frm.serialize(),
			        success: function (data) {
						thisController.formFakeStyle()
						thisController.misc.headerAlert("Response added!","success",5000);
						setTimeout(function(){
							$(".comment-result").empty()
						},7000);
						$(".comment-list").prepend(data);
					},
					error: function(data) {
			        	thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
			        }
				});
			    return false;
			});
			
		},
		removeCommentHandler: function(e)
		{
			e.preventDefault();
			var thisController = this,
			    frm = $(e.currentTarget),
				parent = $(e.currentTarget).parent().parent();
				
			$.ajax({
			    type: frm.attr('method'),
				url: frm.attr('action'),
				data: frm.serialize(),
			    success: function (data) {
					parent.fadeOut();
					thisController.misc.headerAlert("Comment removed!","success",5000);
				},
				error: function(data) {
			        thisController.misc.headerAlert("Something went wrong. Refresh the page and try again!","error",15000);
			    }
			});
		}
	}
});