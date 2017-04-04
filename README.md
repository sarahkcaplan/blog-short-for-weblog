# blog-short-for-weblog
<h2>A Multi-User Blog</h2>
<p>rot13-090117.appspot.com/signup</p>
<h3>Use it to:</h3>
<ul>
  <li>Share your ideas with others</li>
  <li>Read others' ideas</li>
  <li>Like and respond to others' ideas</li>
</ul>
<h3>Getting started on the <a href="rot13-090117.appspot.com/signup">live site</a> is easy:</h3>
<ol>
  <li>Signup</li>
  <li>Read posts on the home page</li>
  <li>Write your own posts</li>
</ol>
<h3>Running the code locally:</h3>
<ol>
  <li>Download the <a href="https://cloud.google.com/sdk/docs/">Google Cloud SDK</a> for your OS</li>
  <li>Extract the gzip file into your home directory</li>
  <li>Run $<code>./google-cloud-sdk/install.sh</code> to install Google Cloud SDK</li>
  <li>Run $<code>gcloud init</code> to initialize GCS</li>
  <li> cd to the blog-short-for-weblog directory cloned to your local machine</li>
  <li>Run $<code>dev_appserver.py .</code> to start local server</li>
  <li>Go to http://localhost:8080/blog to review blog app locally</li>
