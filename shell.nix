with import <nixpkgs> {};
with pkgs.python35Packages;

stdenv.mkDerivation {
  name = "CA645_Continious_assignment_1";

  buildInputs = [
    virtualenv
  ];

  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s)  # so that we can use python wheels
    YELLOW='\033[1;33m'
    NC="$(printf '\033[0m')"

    echo -e "''${YELLOW}Creating python environment...''${NC}"
    virtualenv --no-setuptools venv > /dev/null
    export PATH=$PWD/venv/bin:$PATH > /dev/null
    pip3 install -r requirements.txt > /dev/null
  '';
}