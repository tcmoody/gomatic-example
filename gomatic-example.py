from gomatic import *

configurator = GoCdConfigurator(HostRestClient("gocd-server-lb-504837990.us-east-1.elb.amazonaws.com"))
pipeline_group = configurator.ensure_pipeline_group("Gomatic-Example")
pipeline = pipeline_group.ensure_replacement_of_pipeline("Gomatic-Example")
pipeline.set_git_url("https://github.com/tcmoody/dockerfiles")

docker_build_stage = pipeline.ensure_stage("docker-build")
job = docker_build_stage.ensure_job("docker-build")
job.ensure_resource("docker")
docker_build_task = "docker build . -t gocd-server-image:latest"
job.add_task(ExecTask(['/bin/bash', '-l', '-c', docker_build_task], working_dir="./gocd-server-images/gocd-server-basics"))
configurator.save_updated_config()