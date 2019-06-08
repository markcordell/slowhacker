help:
	/bin/bash -c 'echo help: prod-deploy'
deploy-prod:
	aws s3 cp ./static/styles.css  s3://slowhacker-site/styles.css
	sls deploy && sls invoke -f site-updater
		
deploy-css:
	aws s3 cp ./static/styles.css  s3://slowhacker-site/styles.css
