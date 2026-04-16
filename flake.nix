{
  description = "A Nix flake to run and install Meltdown";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {self, nixpkgs, flake-utils}:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {inherit system;};
        pythonPackages = pkgs.python3Packages;

        # The 'q' package is missing from nixpkgs, so we build it inline from PyPI
        q-debug = pythonPackages.buildPythonPackage rec {
          pname = "q";
          version = "2.7";
          pyproject = true;

          build-system = [
            pythonPackages.setuptools
          ];

          src = pythonPackages.fetchPypi {
            inherit pname version;
            sha256 = "8e0b792f6658ab9e1133b5ea17af1b530530e60124cf9743bc0fa051b8c64f4e";
          };

          doCheck = false;
        };

        # Standard dependencies mapped directly from requirements.txt
        dependencies = [
          q-debug
        ] ++ (with pythonPackages; [
          psutil
          appdirs
          pygments
          pillow
          prompt-toolkit
          rich
          requests
          watchdog
          gitpython
          beautifulsoup4
          litellm
          tkinter # Added Tkinter support here
        ]);

        # Standard CPU llama dependency mapped from llama_reqs.txt
        llamaDependencies = with pythonPackages;
        [
          llama-cpp-python
        ];

        # AMD/Vulkan llama dependency override
        llamaCppPythonVulkan = pythonPackages.llama-cpp-python.overrideAttrs (oldAttrs: {
          nativeBuildInputs = (oldAttrs.nativeBuildInputs or []) ++ [
            pkgs.shaderc # Provides the missing glslc compiler for Vulkan shaders
          ];

          buildInputs = (oldAttrs.buildInputs or []) ++ [
            pkgs.vulkan-headers
            pkgs.vulkan-loader
          ];

          preBuild = (oldAttrs.preBuild or "") + ''
            export CMAKE_ARGS="-DGGML_VULKAN=on"
          '';
        });
        # Helper function to build the application
        mkMeltdown = {extraDeps ?
        [], isVulkan ? false}: pythonPackages.buildPythonApplication {
          pname = "meltdown";
          version = "396.0.0";
          pyproject = true;

          build-system = [
            pythonPackages.hatchling
          ];

          src = ./.;
          propagatedBuildInputs = dependencies ++ extraDeps;

          nativeBuildInputs = [ pkgs.jq ] ++ (
            if isVulkan then
              [ pkgs.makeWrapper ]
            else
              []
          );

          postInstall = ''
            PROGRAM_NAME=$(jq -r '.program' meltdown/manifest.json)
            TITLE=$(jq -r '.title' meltdown/manifest.json)

            mkdir -p $out/share/applications
            mkdir -p $out/share/icons/hicolor/512x512/apps

            cp $PROGRAM_NAME/icon.png $out/share/icons/hicolor/512x512/apps/$PROGRAM_NAME.png

            cat > $out/share/applications/$PROGRAM_NAME.desktop <<EOF
            [Desktop Entry]
            Version=1.0
            Name=$TITLE
            Exec=$out/bin/$PROGRAM_NAME
            Icon=$PROGRAM_NAME
            Terminal=false
            Type=Application
            Categories=Utility;
            EOF
          '' + (
            if isVulkan then
              ''
              # Inject Vulkan loader and rocm-smi paths into the executable
              wrapProgram $out/bin/$PROGRAM_NAME \
                --prefix LD_LIBRARY_PATH : "${pkgs.vulkan-loader}/lib" \
                --prefix PATH : "${pkgs.lib.makeBinPath [ pkgs.rocmPackages.rocm-smi ]}"
              ''
            else
              ""
          );
        };

      in {
        packages = {
          default = mkMeltdown {extraDeps = llamaDependencies;
          isVulkan = false;};
          amd = mkMeltdown {extraDeps = [ llamaCppPythonVulkan ]; isVulkan = true;};
        };

        devShells = {
          default = pkgs.mkShell {
            buildInputs = [
              (pkgs.python3.withPackages (ps: dependencies ++ llamaDependencies ++ [ ps.ruff ps.mypy ]))
              pkgs.pyright
            ];
          };

          amd = pkgs.mkShell {
            nativeBuildInputs = [ pkgs.shaderc ];

            buildInputs = [
              (pkgs.python3.withPackages (ps: dependencies ++ [ llamaCppPythonVulkan ps.ruff ps.mypy ]))
              pkgs.vulkan-headers
              pkgs.vulkan-loader
              pkgs.rocmPackages.rocm-smi
              pkgs.pyright
            ];

            shellHook = ''
              export LD_LIBRARY_PATH="${pkgs.vulkan-loader}/lib:$LD_LIBRARY_PATH"
            '';
          };
        };
      }
    );
}