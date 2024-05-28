# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"
  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python3
    pkgs.pipenv
  ];
  # Sets environment variables in the workspace
  env = {
  };
  idx = {
    workspace.onCreate = {
      pipenv-install = "pipenv install --dev";
    };
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.debugpy"
      "ms-python.python"
    ];
    # Enable previews and customize configuration
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["pipenv" "run" "flask" "--app" "index.py" "--debug" "run" "--host" "0.0.0.0" "--port" "$PORT"];
          manager = "web";
        };
      };
    };
  };
}