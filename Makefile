RPI_WEB_WSGI=/usr/local/rpi_web/wsgi

clean:
	find . -name "*~" | xargs rm -f
	rm -rf doc/_build

deploy:
	mkdir -p $(RPI_WEB_WSGI)
	cp -r wsgi/* $(RPI_WEB_WSGI)

deploy-remote:
	ssh root@$(RPI_WEB_HOST) "mkdir -p $(RPI_WEB_WSGI)"
	rsync -avz -e ssh --delete --exclude '.git' --exclude '.rope*' --exclude '*~' --delete-excluded wsgi/ root@$(RPI_WEB_HOST):$(RPI_WEB_WSGI)
	ssh root@$(RPI_WEB_HOST) "service httpd reload"
