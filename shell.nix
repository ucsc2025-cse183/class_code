let
  nixpkgs-src = builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
    # sha256 = "sha256-checksum-if-known";
  };

  pkgs = import nixpkgs-src {
    config = {
      allowUnfree = true;
      allowBroken = true;
      allowInsecure = true;
      allowUnsupportedSystem = true;
    };
  };

  myPython = pkgs.python311;

  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    pip
    setuptools
    wheel
  ]);

  lib-path = with pkgs; lib.makeLibraryPath [
    libffi
    openssl
  ];

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
      pkgs.qemacs
      pkgs.chromium
      pkgs.chromedriver
      vscodeWithExtensions

      # image and documentation tools
      pkgs.imagemagick

      # packages and libraries
      pythonWithPkgs # Base Python + pip/setuptools/wheel

      # needed for compiling python libs (like psutil, etc if used)
      pkgs.readline
      pkgs.libffi
      pkgs.openssl
      pkgs.gcc
   ];

    shellHook = ''
      SOURCE_DATE_EPOCH=$(date +%s)
      VENV_PATH=.venv
      export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}"

      # --- FONT CONFIGURATION ---
      # Set environment variables so fontconfig knows where to find config
      export FONTCONFIG_FILE=$(find ${pkgs.fontconfig.out}/etc/fonts -name fonts.conf)
      export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts
      echo "Setting FONTCONFIG_FILE=$FONTCONFIG_FILE"
      echo "Setting FONTCONFIG_PATH=$FONTCONFIG_PATH"
      echo "Updating font cache..."
      # Run fc-cache from the fontconfig package provided in buildInputs
      fc-cache -vfs
      echo "Font cache updated."
      # --- END FONT CONFIGURATION ---

      if test ! -d $VENV_PATH; then
        echo "Creating Python virtual environment in $VENV_PATH..."
        python -m venv $VENV_PATH
      fi
      source $VENV_PATH/bin/activate

      echo "Installing/Updating pip packages in venv..."
      $VENV_PATH/bin/pip install -U pip
      $VENV_PATH/bin/pip install -U py4web requests selenium beautifulsoup4 mechanize

      export PS1="\e[30;48;5;214m\u@\h (CSE183) \w [\$(git branch -q --show-current 2>/dev/null)]\e[0m\n$ "
      export EDITOR=nano
      export GIT_EDITOR=nano

      if [ -f "grader/grade.py" ]; then
          alias grade="python $(realpath grader/grade.py)"
      fi
      echo "Nix shell environment ready. Virtual env (.venv) activated."
      echo "Type 'grade <assignment_folder>' to run the grader."
    '';
  };
in shell
