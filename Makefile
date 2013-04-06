all:index.html

index.html: csv/timeline.csv
	timeline-setter -c csv/timeline.csv -o .
	python css/postprocess.py
	rm timeline.html
	cp stylesheets/timeline-setter-custom.css stylesheets/timeline-setter.css
