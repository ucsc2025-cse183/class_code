let
  nixpkgs-src = builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
  };

  pkgs = import nixpkgs-src {
    config = {
      allowUnfree = true;
    };
  };

  # This is the Python version that will be used.
  myPython = pkgs.python311;

  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    pip
    setuptools
    wheel
    isort
    black
    pylint
    pytest
    mechanize
    beautifulsoup4
    selenium
  ]);

  lib-path = with pkgs; lib.makeLibraryPath [
    libffi
    openssl
  ];

  # setup vscode with extensions
  vscodeWithExtensions = (pkgs.vscode-with-extensions.override {
    vscodeExtensions = with pkgs.vscode-extensions; [
      bbenoist.nix
      esbenp.prettier-vscode
      eamodio.gitlens
      ritwickdey.liveserver
      ms-vscode-remote.remote-ssh
      yzhang.markdown-all-in-one
    ];
  });

  shell = pkgs.mkShell {
    buildInputs = [
      # development environment
      pkgs.openssh
      pkgs.zip
      pkgs.mc
      pkgs.git
      pkgs.nano
      pkgs.ungoogled-chromium
      vscodeWithExtensions

      # image and documentation tools
      pkgs.imagemagick
      
      # packages and libraries
      pythonWithPkgs

      # needed for compiling python libs
      pkgs.readline
      pkgs.libffi
      pkgs.openssl
   ];

    shellHook = ''
      # Allow the use of wheels.
      SOURCE_DATE_EPOCH=$(date +%s)
      VENV_PATH=.venv
      # Augment the dynamic linker path
      export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}"

      # Setup the virtual environment if it does not already exist.
      if test ! -d $VENV_PATH; then
        python -m venv $VENV_PATH
      fi      
      if test -f requirements.txt; then
        $VENV_PATH/bin/pip install -U -r requirements.txt
      fi
      $VENV_PATH/bin/pip install -U py4web
      $VENV_PATH/bin/pip install -U requests
      $VENV_PATH/bin/pip install -U webdriver-manager
      source $VENV_PATH/bin/activate
      export PYTHONPATH=$VENV_PATH/${myPython.sitePackages}/:${pythonWithPkgs}/${pythonWithPkgs.sitePackages}:$PYTHONPATH
      export EDITOR=nano
      export GIT_EDITOR=nano
      alias grade=`realpath grader/grade.py`
    '';
  };
in shell
