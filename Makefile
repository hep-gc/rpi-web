RPI_WEB_WSGI=/usr/local/rpi_web/wsgi

clean:
	find . -name "*~" | xargs rm -f
	rm -rf doc/_build

deploy:
	mkdir -p $(RPI_WEB_WSGI)
	cp -r wsgi/* $(RPI_WEB_WSGI)

deploy-remote:
	#ssh -t $(RPI_WEB_HOST) "sudo mkdir -p $(RPI_WEB_WSGI)"
	rsync -avz -e ssh --delete --exclude '.git' --exclude '.rope*' --exclude '*~' --delete-excluded wsgi/ $(RPI_WEB_HOST):$(RPI_WEB_WSGI)
	ssh -t $(RPI_WEB_HOST) "sudo service httpd reload"

deploy-cs-infoserver:
	scp xmlrpc/rpiinfoservers/cloudscheduler_infoserver.py $(CS_INFO_SERVER):bin/

