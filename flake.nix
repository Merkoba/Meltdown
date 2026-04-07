{
  description = "A Nix flake for the Meltdown Python application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonPackages = pkgs.python3Packages;

        # Standard dependencies mapped directly from requirements.txt
        dependencies = with pythonPackages; [
          q
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
        ];

        # Standard CPU llama dependency mapped from llama_reqs.txt
        llamaDependencies = with pythonPackages; [
          llama-cpp-python
        ];

        # AMD/Vulkan llama dependency override
        # This replaces the need for your add_llama_amd.sh script
        llamaCppPythonVulkan = pythonPackages.llama-cpp-python.overrideAttrs (oldAttrs: {
          buildInputs = (oldAttrs.buildInputs or []) ++ [
            pkgs.vulkan-headers
            pkgs.vulkan-loader
          ];
          preBuild = (oldAttrs.preBuild or "") + ''
            export CMAKE_ARGS="-DGGML_VULKAN=on"
          '';
        });

        # Helper function to build the application
        mkMeltdown = { extraDeps ? [], isVulkan ? false }: pythonPackages.buildPythonApplication {
          pname = "meltdown";
          version = "1.0.0"; # Make sure this matches manifest.json
          src = ./.;
          propagatedBuildInputs = dependencies ++ extraDeps;
          nativeBuildInputs = [ pkgs.jq ] ++ (if isVulkan then [ pkgs.makeWrapper ] else []);

          postPatch = ''
            # Prevent setup.py from writing directly to ~/.local
            substituteInPlace setup.py \
              --replace-fail "_post_install()" "print('Skipped custom post-install for Nix build')"
          '';

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
          '' + (if isVulkan then ''
            # Inject Vulkan loader path into the executable
            wrapProgram $out/bin/$PROGRAM_NAME \
              --prefix LD_LIBRARY_PATH : "${pkgs.vulkan-loader}/lib"
          '' else "");
        };

      in {
        packages = {
          default = mkMeltdown { extraDeps = llamaDependencies; isVulkan = false; };
          amd = mkMeltdown { extraDeps = [ llamaCppPythonVulkan ]; isVulkan = true; };
        };

        devShells = {
          default = pkgs.mkShell {
            buildInputs = [
              (pkgs.python3.withPackages (ps: dependencies ++ llamaDependencies))
            ];
          };

          amd = pkgs.mkShell {
            buildInputs = [
              (pkgs.python3.withPackages (ps: dependencies ++ [ llamaCppPythonVulkan ]))
              pkgs.vulkan-headers
              pkgs.vulkan-loader
            ];
            shellHook = ''
              export LD_LIBRARY_PATH="${pkgs.vulkan-loader}/lib:$LD_LIBRARY_PATH"
            '';
          };
        };
      }
    );
}