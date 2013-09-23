<h2>Lend Experience</h2>

This is the Django application for Lend Experience.
<br>
<h4>Applications:</h4>
<ol>
	<li>accounts - User registration, login and forgotten password</li>
	<li>careers - View contributions by career categories, algorithm for assigning careers to categories.</li>
	<li>contributions - handles editing, creating and viewing contribution posts, as well as adding and removing comments (comments should probably be separated out into their own application). Contributions are also known as "experiences" or "experience posts".</li>
	<li>core - location of Template shared by applications.</li>
	<li>lxp - location of settings, urls, wsgi</li>
	<li>search - algorithm for searching contribution posts, people and career tags (tags).</li>
	<li>siteInfo - basic pages: about, contact us, legal etc...</li>
	<li>tags - career tags associated with contribution posts</li>
	<li>text_algorithms - algorithms for text similarity</li>
	<li>userProfile - edit your profile and view profiles. A profile is commonly referred to as a "story".
</ol>
Not included in the application list above, is the `temp` directory, which temporarily holds profile pictures before they're moved over to AWS S3.
<br>
<br>
More detailed information on some of these applications can be found in some of my other repositories:
<ul>
	<li>Text Similarity - <a href="https://github.com/jfmyers/String-Similarity">github.com/jfmyers/String-Similarity</a></li>
	<li>Search Algorithm - <a href="https://github.com/jfmyers/django-redis-autocomplete-search">github.com/jfmyers/django-redis-autocomplete-search</a></li>
</ul>
<h4>Cloud Services:</h4>
<br>
This application uses Amazon SES for email, S3 to store photos, css, js and icons, and Cloudfront for content-delivery.