.PHONY: all build clean

all: build test

clean:
	@rm -rf build dist
	@find .. | grep -E "/__pycache__$$" | xargs rm -rf

build: clean 
	@echo "Building"
	@python3 setup.py py2app

test:
	@echo "Running build"
	@dist/Stone\ Story\ RPG\ Save\ editor.app/Contents/MacOS/Stone\ Story\ RPG\ Save\ editor
