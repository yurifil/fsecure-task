# fsecure-task

Application first prints table of top10 malware detections then starts to print newest detections.

To configure app edit config.json:
```
base_uri - URL to start polling from;
stream_path - path to stream URL obtained in base_uri;
top10_path - path to top10 URL obtained in base_uri;
schema - URL schema to be used with URLs;
http.retry_interval - seconds before next time app will request URL;
http.retries - number of retries;
logdir - path to directory with app logs.
```

To launch application:
```
$ git clone https://github.com/yurifil/fsecure-task.git
$ cd fsecure-task
$ python3 app.py
```

Data is stored in Queue objects and is printed to STDOUT.
