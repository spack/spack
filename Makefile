.PHONY : git pull

git :
	git pull origin
	git push origin

pull :
	git fetch upstream
	git pull upstream develop
