deploy: deploy-dev

dev: deploy-dev
	sls invoke -s dev -f site-updater

deploy-prod: deploy-css-prod
	sls deploy -s prod

deploy-dev: deploy-css-dev
	sls deploy -s dev
		
deploy-css-prod:
	aws s3 cp ./static/styles.css  s3://slowhacker.com/styles.css

deploy-css-dev:
	aws s3 cp ./static/styles.css  s3://dev.slowhacker.com/styles.css
