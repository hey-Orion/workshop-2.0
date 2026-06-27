import yaml

yaml_content = """
dev:
   debug: true
pro:
   debug: false
"""

config = yaml.safe_load(yaml_content)
current_env = "pro"
is_debug = config[current_env]["debug"]



import yaml

pipeline_runer_S = {
    "e_date": "2",
    "status": "success",
    "records": 4050
}

with open("run_report.yaml", "w") as file:
    yaml.dump(pipeline_runer_S, file, default_flow_style=False)



import yaml

yaml_str = """
db: 
  host: "localhost"
  port: 5432
  creds:
    user: "orion
"""

config = yaml.safe_load(yaml_str)
db_port = config["db"]["creds"]["user"]




import yaml 

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file) or {}

api_config = config.get("api", {})
url = api_config.get("url", "https://fallback-url.com")
timeout = api_config.get("timeout_sec", 10)



import yaml

with open("config.yaml", "r") as file:
    try:
        config = yaml.safe_load(file)
        url = config["api"]["url"]
        timeout = config["api"]["timeout_seconds"]
        token = config["api"]["auth_token"]
        print(f"Loaded configuration for {url}")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")