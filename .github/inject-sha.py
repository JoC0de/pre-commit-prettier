import sys
import yaml

THIS_REPO = "https://github.com/JoC0de/pre-commit-prettier"
ROOT_REPO_NAME = "JoC0de/pre-commit-prettier"
PRE_COMMIT_CONFIG = ".pre-commit-config.yaml"


def main(sha: str, repo_name: str = ROOT_REPO_NAME) -> None:
    """Inject the SHA into the YAML file."""
    # Load the YAML file
    with open(PRE_COMMIT_CONFIG, "r", encoding="utf-8") as fo:
        config = yaml.safe_load(fo)

    # Inject the SHA into the config
    for i, repo in enumerate(config.get("repos", [])):
        if repo.get("repo") != THIS_REPO:
            continue
        print(f"Injecting SHA `{sha}` into repo {repo}")
        config["repos"][i]["rev"] = sha
        if repo_name != ROOT_REPO_NAME:
            repo_name = repo["repo"].replace(ROOT_REPO_NAME, repo_name)
            print(f"Updating repo URL to {repo_name}")
            config["repos"][i]["repo"] = repo_name

    # Save the updated config back to the file
    with open(PRE_COMMIT_CONFIG, "w", encoding="utf-8") as fo:
        yaml.safe_dump(config, fo, default_flow_style=False)


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python inject-sha.py <sha> [optional:<repo-name>]")
        sys.exit(1)

    sha = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else ROOT_REPO_NAME
    main(sha=sha, repo_name=repo)
    print(f"SHA `{sha}` and repo `{repo}` injected into .pre-commit-config.yaml")
