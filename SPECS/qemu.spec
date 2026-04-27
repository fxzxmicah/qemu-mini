%global qemu_epoch 2
%global keycodemapdb_commit f5772a62ec52591ff6870b7e8ef32482371f22c6

Name:           qemu
Epoch:          %{qemu_epoch}
Version:        11.0.0
Release:        1%{?dist}
Summary:        Minimal QEMU system emulator for KVM guests

License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND FSFAP AND GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-2.0-or-later WITH GCC-exception-2.0 AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND MIT AND LicenseRef-Fedora-Public-Domain AND CC-BY-3.0
URL:            https://www.qemu.org/
Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
Source1:        https://gitlab.com/qemu-project/keycodemapdb/-/archive/%{keycodemapdb_commit}/keycodemapdb-%{keycodemapdb_commit}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  sed
BuildRequires:  systemd-rpm-macros
BuildRequires:  tar
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(liburing)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(slirp)
BuildRequires:  pkgconfig(virglrenderer)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(zlib)

Provides:       qemu-common = %{qemu_epoch}:%{version}-%{release}
Provides:       qemu-system-x86 = %{qemu_epoch}:%{version}-%{release}
Provides:       qemu-system-x86-core = %{qemu_epoch}:%{version}-%{release}
Provides:       qemu-ui-gtk = %{qemu_epoch}:%{version}-%{release}
Provides:       qemu-audio-pipewire = %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-common < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-system-x86 < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-system-x86-core < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-ui-gtk < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-ui-sdl < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-alsa < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-dbus < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-jack < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-oss < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-pa < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-pipewire < %{qemu_epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-sdl < %{qemu_epoch}:%{version}-%{release}

%description
This package is a deliberately small QEMU build for running x86_64 guests on a
Linux KVM host.  It keeps the system emulator, direct Linux kernel/initramfs
boot, virtio storage/network/input/display/sound, libslirp user-mode NAT, GTK
display output, and OpenGL/virgl acceleration.

It intentionally omits user-mode emulators, most architecture targets, TCG,
guest agent, qemu-img/tools, firmware blobs, external network backends, VNC,
SPICE, USB passthrough, TPM, Xen, VFIO, and most legacy device models.

%prep
%autosetup -n qemu-%{version} -p1

if [ ! -d subprojects/keycodemapdb ]; then
    tar -xf %{SOURCE1} -C subprojects
    mv subprojects/keycodemapdb-%{keycodemapdb_commit} subprojects/keycodemapdb
fi

cat > configs/devices/x86_64-softmmu/minimal.mak <<'EOF'
# Minimal x86_64 KVM profile.
CONFIG_Q35=y

CONFIG_VIRTIO_PCI=y
CONFIG_VIRTIO_BLK=y
CONFIG_VIRTIO_SCSI=y
CONFIG_VIRTIO_NET=y
CONFIG_VIRTIO_RNG=y
CONFIG_VIRTIO_BALLOON=y
CONFIG_VIRTIO_INPUT=y
CONFIG_VIRTIO_GPU=y
CONFIG_VIRTIO_VGA=y
CONFIG_VIRTIO_SND=y
CONFIG_VIRTIO_SERIAL=y
EOF

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --datadir=%{_datadir} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}/%{name} \
    --target-list=x86_64-softmmu \
    --without-default-features \
    --without-default-devices \
    --with-devices-x86_64=minimal \
    --enable-system \
    --disable-user \
    --disable-linux-user \
    --disable-bsd-user \
    --enable-kvm \
    --disable-tcg \
    --disable-hvf \
    --disable-mshv \
    --disable-nvmm \
    --disable-whpx \
    --disable-xen \
    --disable-xen-pci-passthrough \
    --enable-slirp \
    --disable-passt \
    --disable-af-xdp \
    --disable-l2tpv3 \
    --disable-netmap \
    --disable-vde \
    --disable-vhost-user \
    --disable-vhost-vdpa \
    --enable-vhost-kernel \
    --enable-vhost-net \
    --enable-gtk \
    --disable-sdl \
    --disable-curses \
    --disable-vnc \
    --disable-spice \
    --disable-dbus-display \
    --enable-opengl \
    --enable-virglrenderer \
    --disable-rutabaga-gfx \
    --enable-pixman \
    --enable-png \
    --enable-xkbcommon \
    --audio-drv-list=pipewire \
    --enable-pipewire \
    --disable-alsa \
    --disable-pa \
    --disable-jack \
    --disable-oss \
    --disable-tools \
    --disable-guest-agent \
    --disable-docs \
    --disable-install-blobs \
    --disable-modules \
    --disable-plugins \
    --disable-rdma \
    --disable-replication \
    --disable-tpm \
    --disable-smartcard \
    --disable-u2f \
    --disable-canokey \
    --disable-libusb \
    --disable-usb-redir \
    --disable-virtfs \
    --disable-vfio-user-server \
    --disable-multiprocess \
    --enable-linux-io-uring \
    --disable-auth-pam \
    --disable-brlapi \
    --disable-capstone \
    --disable-curl \
    --disable-fuse \
    --disable-glusterfs \
    --disable-libiscsi \
    --disable-libnfs \
    --disable-libssh \
    --disable-mpath \
    --disable-rbd \
    --disable-bochs \
    --disable-cloop \
    --disable-dmg \
    --disable-qcow1 \
    --disable-qed \
    --disable-parallels \
    --disable-vdi \
    --disable-vhdx \
    --disable-vmdk \
    --disable-vpc \
    --disable-vvfat \
    --disable-bzip2 \
    --disable-lzfse \
    --disable-lzo \
    --disable-snappy \
    --disable-zstd \
    --disable-qatzip \
    --disable-qpl \
    --disable-uadk \
    --disable-blkio \
    --disable-libpmem \
    --disable-libdaxctl \
    --disable-numa \
    --disable-seccomp \
    --disable-selinux \
    --disable-gnutls \
    --disable-gcrypt \
    --disable-nettle \
    --disable-keyring \
    --disable-libkeyutils \
    --disable-bpf \
    --disable-attr \
    --disable-libudev \
    --disable-libdw \
    --disable-igvm \
    --disable-rust \
    --disable-werror
%make_build

%install
%make_install

find %{buildroot} -name '*.la' -delete

install -Dpm 0644 /dev/stdin %{buildroot}%{_sysusersdir}/qemu.conf <<'EOF'
g kvm 36
u qemu 107 'qemu user' - -
m qemu kvm
EOF

%check
# Build tests are not run for this minimal package.

%files
%license COPYING COPYING.LIB LICENSE
%doc README.rst
%{_bindir}/qemu-system-x86_64
%{_datadir}/qemu/
%{_datadir}/applications/qemu.desktop
%{_datadir}/icons/hicolor/*/apps/qemu.*
%{_sysusersdir}/qemu.conf

%changelog
* Mon Apr 27 2026 Fxzx micah <48860358+fxzxmicah@users.noreply.github.com> - 2:11.0.0-1
- Minimal x86_64 KVM build for direct kernel/initramfs boot,
  virtio devices, slirp NAT, GTK display, PipeWire audio, and virgl.
- https://github.com/fxzxmicah/qemu-mini/
