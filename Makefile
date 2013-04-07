all:index.html

index.html: csv/timeline.csv
	timeline-setter -c csv/timeline.csv -o .
	python csv/postprocess.py
	rm timeline.html
