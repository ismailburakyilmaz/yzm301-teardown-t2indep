#!/bin/sh
# Online bootstrap or an explicit offline wheel + complete wheelhouse/cache.
set -eu
project_dir=$(CDPATH= cd -P "$(dirname "$0")" && pwd)
destination="$project_dir/.run"
python_version=3.14.8
python_executable=
uv_executable=
offline=0
wheel=
wheelhouse=
cache=
no_path=0
while [ "$#" -gt 0 ]; do
    case "$1" in
        --offline) offline=1; shift ;;
        --no-path) no_path=1; shift ;;
        --destination|--python-version|--python|--uv|--wheel|--wheelhouse|--cache-dir)
            [ "$#" -ge 2 ] || { echo "Missing value for $1" >&2; exit 2; }
            case "$1" in
                --destination) destination=$2 ;; --python-version) python_version=$2 ;;
                --python) python_executable=$2 ;; --uv) uv_executable=$2 ;;
                --wheel) wheel=$2 ;; --wheelhouse) wheelhouse=$2 ;; --cache-dir) cache=$2 ;;
            esac
            shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done
mkdir -p "$destination"
destination=$(CDPATH= cd -P "$destination" && pwd)
if [ "$offline" -eq 1 ]; then
    [ -n "$python_executable" ] && [ -n "$uv_executable" ] && [ -f "$wheel" ] || {
        echo 'Offline mode requires --python, --uv and --wheel; supply a complete compatible wheelhouse or populated uv cache.' >&2; exit 2;
    }
fi
if [ -z "$uv_executable" ]; then
    uv_executable="$destination/.tools/uv/uv"
    if [ ! -x "$uv_executable" ]; then
        mkdir -p "$destination/.tools/uv"
        curl -LsSf https://astral.sh/uv/0.13.4/install.sh -o "$destination/.tools/uv-install.sh"
        UV_UNMANAGED_INSTALL="$destination/.tools/uv" UV_NO_MODIFY_PATH=1 sh "$destination/.tools/uv-install.sh"
    fi
fi
export UV_CACHE_DIR=${cache:-"$destination/.cache"}
export UV_PYTHON_INSTALL_DIR="$destination/.tools/python"
export UV_PYTHON_BIN_DIR="$destination/.tools/python-bin"
export UV_PYTHON_INSTALL_REGISTRY=false
if [ "$offline" -eq 1 ]; then export UV_OFFLINE=1; fi
if [ -z "$python_executable" ]; then
    "$uv_executable" python install "$python_version"
    python_executable=$("$uv_executable" python find --managed-python "$python_version")
fi
if [ ! -x "$destination/.venv/bin/python" ]; then
    [ ! -e "$destination/.venv" ] || { echo 'Existing destination has no usable venv Python; choose another destination.' >&2; exit 2; }
    "$uv_executable" venv --python "$python_executable" "$destination/.venv"
fi
python_executable="$destination/.venv/bin/python"
"$python_executable" "$project_dir/scripts/platform_lock.py" "$project_dir/requirements.lock.txt" "$destination/requirements.platform.lock.txt"
set -- pip install --compile-bytecode --link-mode copy --python "$python_executable"
if [ -n "$wheelhouse" ]; then set -- "$@" --no-index --find-links "$wheelhouse"; fi
"$uv_executable" "$@" -r "$destination/requirements.platform.lock.txt"
if [ -n "$wheel" ]; then
    "$uv_executable" "$@" --no-deps "$wheel"
else
    "$uv_executable" "$@" --no-deps --no-build-isolation "$project_dir"
fi
# Probe bytecode without importing SciPy, then make exactly one real CLI calculation.
"$python_executable" -I "$project_dir/scripts/prepare_runtime.py" \
    --cli "$destination/.venv/bin/gpower-clone" \
    --receipt "$destination/PREPARATION_RECEIPT.json" \
    --probe "$destination/PREPARATION_PYCACHE_BEFORE.json"
"$uv_executable" pip check --python "$python_executable"
# Preparation is an explicitly timed installation cost, not a hidden first call.
"$destination/.venv/bin/gpower-clone" --version
if [ "$no_path" -eq 0 ]; then
    mkdir -p "$HOME/.local/bin"
    link="$HOME/.local/bin/gpower-clone"
    if [ -e "$link" ] && [ ! -L "$link" ]; then
        echo "Refusing to replace existing non-symlink $link" >&2; exit 2
    fi
    ln -sfn "$destination/.venv/bin/gpower-clone" "$link"
    echo "User launcher link: $link -> $destination/.venv/bin/gpower-clone"
    case ":$PATH:" in *":$HOME/.local/bin:"*) : ;; *) echo "$HOME/.local/bin is not in PATH. For this shell: export PATH=\"\$HOME/.local/bin:\$PATH\"" ;; esac
fi
echo "Installed in $destination/.venv."
echo 'No shell profile or persistent PATH was changed.'
