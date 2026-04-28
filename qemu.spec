%global keycodemapdb_commit f5772a62ec52591ff6870b7e8ef32482371f22c6
%global qemu_arch %{lua:local arch = rpm.expand("%{_arch}"); local map = "x86_64=x86_64;aarch64=aarch64;ppc64le=ppc64;riscv64=riscv64;s390x=s390x;loongarch64=loongarch64"; for pair in string.gmatch(map, "[^;]+") do local eq = string.find(pair, "="); local rpm_arch = string.sub(pair, 1, eq - 1); local qemu_arch = string.sub(pair, eq + 1); if arch == rpm_arch then print(qemu_arch); return end end; print(arch)}
%global qemu_package_arch %{lua:local arch = rpm.expand("%{_arch}"); local map = "x86_64=x86;aarch64=aarch64;ppc64le=ppc;riscv64=riscv;s390x=s390x;loongarch64=loongarch64"; for pair in string.gmatch(map, "[^;]+") do local eq = string.find(pair, "="); local rpm_arch = string.sub(pair, 1, eq - 1); local package_arch = string.sub(pair, eq + 1); if arch == rpm_arch then print(package_arch); return end end; print(arch)}

Name:           qemu
Epoch:          2
Version:        11.0.0
Release:        1%{?dist}
Summary:        Minimal QEMU system emulator for KVM guests

License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND FSFAP AND GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-2.0-or-later WITH GCC-exception-2.0 AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND MIT AND LicenseRef-Fedora-Public-Domain AND CC-BY-3.0
URL:            https://www.qemu.org/
Source0:        https://download.qemu.org/qemu-%{version}.tar.xz
Source1:        https://gitlab.com/qemu-project/keycodemapdb/-/archive/%{keycodemapdb_commit}/keycodemapdb-%{keycodemapdb_commit}.tar.gz

Patch1:         donot-depend-on-cxl.patch

ExclusiveArch:  x86_64 aarch64 ppc64le riscv64 s390x loongarch64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
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

Provides:       qemu-common = %{epoch}:%{version}-%{release}
Provides:       qemu-system-%{qemu_package_arch} = %{epoch}:%{version}-%{release}
Provides:       qemu-system-%{qemu_package_arch}-core = %{epoch}:%{version}-%{release}
Provides:       qemu-ui-gtk = %{epoch}:%{version}-%{release}
Provides:       qemu-audio-pipewire = %{epoch}:%{version}-%{release}
Obsoletes:      qemu-common < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-system-%{qemu_package_arch} < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-system-%{qemu_package_arch}-core < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-ui-gtk < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-ui-sdl < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-alsa < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-dbus < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-jack < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-oss < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-pa < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-pipewire < %{epoch}:%{version}-%{release}
Obsoletes:      qemu-audio-sdl < %{epoch}:%{version}-%{release}

%description
This package is a deliberately small QEMU build for running native KVM guests
on a Linux host.  It keeps the system emulator, direct Linux kernel/initramfs
boot, virtio storage/network/input/display/sound, libslirp user-mode NAT, GTK
display output, and OpenGL/virgl acceleration.

It intentionally omits user-mode emulators, non-native architecture targets,
TCG, guest agent, qemu-img/tools, non-native firmware blobs, external network
backends, VNC, SPICE, USB passthrough, TPM, Xen, VFIO, and most legacy device
models.

%prep
%autosetup -n qemu-%{version} -p1

if [ ! -d subprojects/keycodemapdb ]; then
    tar -xf %{SOURCE1} -C subprojects
    mv subprojects/keycodemapdb-%{keycodemapdb_commit} subprojects/keycodemapdb
fi

cat > configs/devices/%{qemu_arch}-softmmu/minimal.mak <<'EOF'
# Minimal KVM profile.
%ifarch x86_64
CONFIG_Q35=y
%endif
%ifarch aarch64
CONFIG_ARM_VIRT=y
%endif
%ifarch riscv64
CONFIG_RISCV_VIRT=y
%endif
%ifarch ppc64le
CONFIG_PSERIES=y
%endif
%ifarch s390x
CONFIG_S390_CCW_VIRTIO=y
CONFIG_VIRTIO_CCW=y
%endif
%ifarch loongarch64
CONFIG_LOONGARCH_VIRT=y
%endif

CONFIG_VIRTIO_PCI=y
CONFIG_VIRTIO_BLK=y
CONFIG_VIRTIO_SCSI=y
CONFIG_VIRTIO_NET=y
CONFIG_VIRTIO_RNG=y
CONFIG_VIRTIO_BALLOON=y
CONFIG_VIRTIO_INPUT=y
CONFIG_VIRTIO_GPU=y
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
    --disable-download \
    --target-list=%{qemu_arch}-softmmu \
    --without-default-features \
    --without-default-devices \
    --with-devices-%{qemu_arch}=minimal \
    --disable-qom-cast-debug \
    --disable-relocatable \
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
    --enable-trace-backends=nop \
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
rm -rf %{buildroot}%{_datadir}/qemu/dtb

install -d %{buildroot}%{_datadir}/qemu/firmware

%ifarch x86_64 riscv64 ppc64le s390x
for f in \
%ifarch x86_64
    bios-256k.bin \
    bios.bin \
    kvmvapic.bin \
    linuxboot_dma.bin \
    multiboot_dma.bin \
    pvh.bin \
    vgabios-ramfb.bin \
    pxe-virtio.rom \
    efi-virtio.rom
%endif
%ifarch riscv64
    opensbi-riscv64-generic-fw_dynamic.bin
%endif
%ifarch ppc64le
    slof.bin \
    vof.bin
%endif
%ifarch s390x
    s390-ccw.img
%endif
do
    install -pm 0644 pc-bios/${f} %{buildroot}%{_datadir}/qemu/${f}
done
%endif

%ifarch x86_64 aarch64 riscv64 loongarch64
for f in \
%ifarch x86_64
    edk2-x86_64-code.fd \
    edk2-x86_64-secure-code.fd \
    edk2-i386-vars.fd
%endif
%ifarch aarch64
    edk2-aarch64-code.fd \
    edk2-arm-vars.fd
%endif
%ifarch riscv64
    edk2-riscv-code.fd \
    edk2-riscv-vars.fd
%endif
%ifarch loongarch64
    edk2-loongarch64-code.fd \
    edk2-loongarch64-vars.fd
%endif
do
    install -pm 0644 build/pc-bios/${f} %{buildroot}%{_datadir}/qemu/${f}
done

for f in \
%ifarch x86_64
    50-edk2-x86_64-secure.json \
    60-edk2-x86_64.json
%endif
%ifarch aarch64
    60-edk2-aarch64.json
%endif
%ifarch riscv64
    60-edk2-riscv64.json
%endif
%ifarch loongarch64
    60-edk2-loongarch64.json
%endif
do
    sed 's|@DATADIR@|%{_datadir}/qemu|g' pc-bios/descriptors/${f} \
        > %{buildroot}%{_datadir}/qemu/firmware/${f}
done
%endif

for f in \
%ifarch x86_64
    bios-256k.bin \
    bios.bin \
    kvmvapic.bin \
    linuxboot_dma.bin \
    multiboot_dma.bin \
    pvh.bin \
    vgabios-ramfb.bin \
    pxe-virtio.rom \
    efi-virtio.rom \
    edk2-x86_64-code.fd \
    edk2-x86_64-secure-code.fd \
    edk2-i386-vars.fd \
    firmware/50-edk2-x86_64-secure.json \
    firmware/60-edk2-x86_64.json
%endif
%ifarch aarch64
    edk2-aarch64-code.fd \
    edk2-arm-vars.fd \
    firmware/60-edk2-aarch64.json
%endif
%ifarch riscv64
    opensbi-riscv64-generic-fw_dynamic.bin \
    edk2-riscv-code.fd \
    edk2-riscv-vars.fd \
    firmware/60-edk2-riscv64.json
%endif
%ifarch ppc64le
    slof.bin \
    vof.bin
%endif
%ifarch s390x
    s390-ccw.img
%endif
%ifarch loongarch64
    edk2-loongarch64-code.fd \
    edk2-loongarch64-vars.fd \
    firmware/60-edk2-loongarch64.json
%endif
do
    test -f %{buildroot}%{_datadir}/qemu/${f}
done

install -Dpm 0644 /dev/stdin %{buildroot}%{_sysusersdir}/qemu.conf <<'EOF'
g kvm 36
u qemu 107 'qemu user' - -
m qemu kvm
EOF

%check
# Build tests are not run for this minimal package.

%files
%license COPYING COPYING.LIB LICENSE
%ifarch x86_64 aarch64 riscv64 loongarch64
%license pc-bios/edk2-licenses.txt
%endif
%doc README.rst
%{_bindir}/qemu-system-%{qemu_arch}
%{_datadir}/qemu/
%{_datadir}/applications/qemu.desktop
%{_datadir}/icons/hicolor/*/apps/qemu.*
%{_sysusersdir}/qemu.conf

%changelog
* Mon Apr 27 2026 Fxzx micah <48860358+fxzxmicah@users.noreply.github.com> - 2:11.0.0-1
- Minimal KVM build for direct kernel/initramfs boot,
  virtio devices, slirp NAT, GTK display, PipeWire audio, and virgl.
- https://github.com/fxzxmicah/qemu-mini/
