{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = with pkgs; [
    sonar-scanner-cli
    sqlite
  ];
}
