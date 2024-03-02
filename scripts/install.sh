#!/usr/bin/env bash

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"

content=$(cat <<EOF
#!/usr/bin/env bash
$parent/venv/bin/python $parent/src/main.py "\${@}"
EOF
)

echo "$content" > /tmp/gifmakergui_tmp.sh
sudo sudo mv /tmp/gifmakergui_tmp.sh /usr/bin/gifmakergui
sudo sudo chmod +x /usr/bin/gifmakergui
echo "Script created at /usr/bin/gifmakergui"