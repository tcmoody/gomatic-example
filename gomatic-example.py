from gomatic import *

configurator = GoCdConfigurator(HostRestClient("gocd-server-lb-504837990.us-east-1.elb.amazonaws.com"))
pipeline_group = configurator.ensure_pipeline_group("Gomatic-Example")

# docker lint
docker_lint_pipeline = pipeline_group.ensure_replacement_of_pipeline("Docker-Lint")
docker_lint_pipeline.set_git_url("https://github.com/tcmoody/dockerfiles")

docker_lint_stage = docker_lint_pipeline.ensure_stage("docker-lint")
docker_lint_job = docker_lint_stage.ensure_job("docker-lint")
docker_lint_job.ensure_resource("docker")
docker_lint_task = "/tmp/hadolint dockerfile"
docker_lint_job.add_task(ExecTask(['/bin/bash', '-l', '-c', docker_lint_task], working_dir="./gocd-server-images/gocd-server-basics"))
docker_lint_job.ensure_artifacts({BuildArtifact(src='gocd-server-images/gocd-server-basics/dockerfile')})

# docker build
docker_build_pipeline = pipeline_group.ensure_replacement_of_pipeline("Docker-Build")
docker_build_pipeline.ensure_material(PipelineMaterial('Docker-Lint', 'docker-lint'))
# docker_build_pipeline.set_git_url("https://github.com/tcmoody/dockerfiles")

docker_build_stage = docker_build_pipeline.ensure_stage("docker-build")
docker_build_job = docker_build_stage.ensure_job("docker-build")
docker_build_job.ensure_resource("docker")
docker_build_job.add_task(FetchArtifactTask(pipeline="docker-lint", stage="docker-lint", job="docker-lint", src=(FetchArtifactFile("dockerfile")), origin="gocd"))

docker_build_task = "docker build . -t gocd-server-image:latest"

docker_build_job.add_task(ExecTask(['/bin/bash', '-l', '-c', docker_build_task]))
configurator.save_updated_config()