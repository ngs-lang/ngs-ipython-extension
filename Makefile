default:
	@echo "No target specified"
	exit 1

.PHONY: docker-build
docker-build:
	docker build -t ngslang/ngs-jupyter .

.PHONY: docker-run
docker-run:
	docker run -p 8888:8888 ngslang/ngs-jupyter
