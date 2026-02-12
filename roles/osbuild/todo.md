# todo

refactor role to use image-builder CLI instead of composer-cli

- create a jinja2 template(s) for the blueprint file(s)
- consoldiate all package lists in the entire collection to a single source that both the image-builder and ansible-pull can use


`sudo image-builder build minimal-installer --distro fedora-43 --extra-repo "https://developer.download.nvidia.com/compute/cuda/repos/fedora42/x86_64" --extra-repo "http://dl.google.com/linux/chrome/rpm/stable/x86_64" --extra-repo "https://us-central1-yum.pkg.dev/projects/antigravity-auto-updater-dev/antigravity-rpm" --extra-repo "https://download.opensuse.org/repositories/home:/TheLocehiliosan:/yadm/Fedora_43/" --blueprint workstation/fedora-43-workstation-nvidia.toml`