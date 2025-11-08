# main.py
from dotenv import load_dotenv
from orchestrator.pipeline_orchestrator import PipelineOrchestrator
from pipelines.factory import PipelineFactory

load_dotenv()

def main():
    yaml_path = "config/pipelines.yaml"
    pipelines = PipelineFactory.build_pipelines_from_yaml(yaml_path)

    orchestrator = PipelineOrchestrator(pipelines=pipelines, parallel=False, max_retries=3)
    orchestrator.run()

if __name__ == "__main__":
    main()