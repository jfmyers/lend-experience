/*global Backbone */
var app = app || {};

(function () {
	'use strict';
	app.Router = Backbone.Router.extend({
		//routes: {},
		initialize: function(){
			//var router = this,
			this.route(/^([0-9A-Za-z]+)-([0-9A-Za-z]+)-([0-9A-Za-z]+)$/,"story")
			this.route(/^career\/([0-9A-Za-z]+)$/,"career")
			/*routess = [
				[ /^([0-9A-Za-z]+)-([0-9A-Za-z]+)-([0-9A-Za-z]+)$/, 'story' ],
				[ 'story/view', 'story'],
				[ 'story/edit', 'editMyStory' ],
				['*actions', "defaultRoute"]
			];
			_.each(routess, function(route) { 
				//console.log(route)
				console.log(route[0])
				router.route(route[0],route[1])
				//router.route.apply(router,route); 
			})*/
		},
		routes: {
			'story/view'	  		  		  : 		'story',
			'story/edit'	  		  		  : 		'editMyStory',
			'*actions'			  			  : 		'defaultRoute'
		},
		editMyStory: function(){
			window.scrollTo(0,0);
			app.editMyStory = app.EditStoryController;
			app.editMyStory.init()
		},
		story: function(){
			window.scrollTo(0,0);
			app.story = app.StoryController;
			app.story.init()
		},
		career: function(){
			window.scrollTo(0,0);
			app.career = app.CareerController;
			app.career.init()
		},
		singleContribution: function(){
			window.scrollTo(0,0);
			app.singleContribution = app.SingleContributionController;
			app.singleContribution.init()
		},
		defaultRoute: function(){
			if(page == "story") {
				app.story = app.StoryController;
				app.story.init()
				
			} else if(page == "myStory") {
				app.story = app.StoryController;
				app.story.init()
				
			} else if(page == "editStory") {
				app.editMyStory = app.EditStoryController;
				app.editMyStory.init()
				
			} else if(page == "career") {
				app.career = app.CareerController;
				app.career.init()
				
			} else if(page == "singleContribution"){
				app.singleContribution = app.SingleContributionController;
				app.singleContribution.init()
				
			} else if(page == "add_contribution"){
				app.addContribution = app.AddContributionController;
				app.addContribution.init()
				
			} else if(page == "edit_contribution"){
				app.editContribution = app.EditContributionController;
				app.editContribution.init()
				
			} else{
				app.contributions = app.ContributionsController;
				app.contributions.init()
			}
		}

	});

	
})();
