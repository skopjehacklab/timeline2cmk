all:index.html

index.html: csv/timeline.csv
	timeline-setter -c csv/timeline.csv -o .
	mv timeline.html index.html
