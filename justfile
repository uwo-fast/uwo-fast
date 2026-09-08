# Task runner for the UWO-FAST general repository.
# Run `just` on its own to list recipes.
#
# The lab signs are the only build pipeline here; the other top-level
# directories (agri-tunnel-sign, teb-6-7-layout, printing-profiles) are asset
# stores with nothing to build.
#
# The build shells out to pandoc, lualatex, pdftoppm and mmdc. A missing one of
# those is the usual cause of a confusing failure -- `just tools` reports which.
#
# `just sign` rebuilds the combined PDF and manifest.json from only the signs
# named, so follow it with `just build` to restore them for the whole set.

# Use the project venv once it exists, so recipes work before and after `just setup`.
python := if path_exists(".venv/bin/python") == "true" { ".venv/bin/python" } else { "python3" }

# List available recipes.
default:
    @just --list

# Create .venv and install the Python and Node dependencies.
setup:
    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install -r requirements.txt
    npm ci

# Build every lab sign PDF into output/lab-signs. Same command CI runs.
build:
    {{ python }} scripts/build_lab_signs.py --all

# Build only the named signs, e.g. `just sign lab-signs/sink.md`.
sign +SIGNS:
    {{ python }} scripts/build_lab_signs.py {{ SIGNS }}

# Build every sign plus PNG page previews in artifacts/lab-signs/png.
preview:
    {{ python }} scripts/build_lab_signs.py --all --png

# CI equivalent: a clean full build must succeed. Run before committing.
check: clean build

# Show the page count of each built sign.
pages:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! compgen -G "output/lab-signs/*.pdf" > /dev/null; then
        echo "No built signs found. Run 'just build' first." >&2
        exit 1
    fi
    for pdf in output/lab-signs/*.pdf; do
        printf '%-38s %s\n' "$(basename "$pdf" .pdf)" "$(pdfinfo "$pdf" | awk '/^Pages/ {print $2}')"
    done

# Check that the external PDF toolchain is installed.
tools:
    #!/usr/bin/env bash
    missing=0
    for tool in pandoc lualatex pdftoppm; do
        if command -v "$tool" > /dev/null; then
            printf '  ok       %s\n' "$tool"
        else
            printf '  MISSING  %s\n' "$tool"
            missing=1
        fi
    done
    if [ -x node_modules/.bin/mmdc ]; then
        printf '  ok       mmdc (node_modules)\n'
    else
        printf '  MISSING  mmdc -- run: just setup\n'
        missing=1
    fi
    exit "$missing"

# Delete generated build output.
clean:
    rm -rf output artifacts
