# Fetch Process Lambda

Lambda function for downloading and processing arbitrary data files

## Use

```bash
make clean
make fetch-process-lambda ARGS=<python_library>
```

Deploy `dist/` contents as a zip for lambda.

## TODO

* Remove numpy and pandas dependencies