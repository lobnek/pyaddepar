
.PHONY: tag
tag:
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags

