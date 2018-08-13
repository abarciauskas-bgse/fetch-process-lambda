clean:
	rm -rf dist

dist:
	mkdir -p dist

requirements: dist requirements.txt
	pip3 install -r requirements.txt --target ./dist/ --no-cache-dir
	pip3 install ${ARGS} --target ./dist --no-cache-dir
	echo ${ARGS} > process_function.txt
	find ./dist -type d -name '__pycache__' | xargs rm -rf
	rm -rf dist/docutils

fetch-process: requirements
	cp lambda_function.py ./dist/
	cp process_function.txt ./dist/
