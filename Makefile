clean:
	rm -rf dist

dist:
	mkdir -p dist

requirements: dist requirements.txt
	/Users/aimeebarciauskas/anaconda2/bin/pip install -r requirements.txt --target ./dist/ --no-cache-dir
	/Users/aimeebarciauskas/anaconda2/bin/pip install ${ARGS} --target ./dist --no-cache-dir
	echo ${ARGS} > process_function.txt
	find ./dist -type d -name '__pycache__' | xargs rm -rf
	rm -rf dist/docutils

fetch-process: requirements
	cp lambda_function.py ./dist/
	cp process_function.txt ./dist/
