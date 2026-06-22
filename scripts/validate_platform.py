import sys
import yaml
from pathlib import Path

VALID_STACKS = ["python", "node", "dotnet"]
VALID_SERVICES = ["container_app", "key_vault", "sql_database", "storage"]

REQUIRED_FIELDS = [
    "app_name",
    "team",
    "stack",
    "services",
    "registry",
    "environments",
]

def main():
    config_path = Path("app/platform.yml")

    if not config_path.exists():
        print("platform.yml not found at app/platform.yml")
        sys.exit(1)

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    errors = []

    for field in REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Missing required field: {field}")

    if config.get("stack") not in VALID_STACKS:
        errors.append(f"Invalid stack: {config.get('stack')}")

    for service in config.get("services", []):
        if service not in VALID_SERVICES:
            errors.append(f"Invalid service: {service}")

    if "registry" in config and "name" not in config["registry"]:
        errors.append("Missing registry.name")

    required_envs = ["dev", "staging", "prod"]

    for env in required_envs:
        if env not in config["environments"]:
            errors.append(f"Missing environment: {env}")

    for env in required_envs:
        if "resource_group" not in config["environments"][env]:
            errors.append(
                f"Missing resource_group in environments.{env}"
            )

    if not config.get("environments"):
        errors.append("At least one environment is required")

    if errors:
        print("platform.yml validation FAILED")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("platform.yml is valid")

if __name__ == "__main__":
    main()