#!/usr/bin/env bash
# DeskMate 跨平台打包脚本 / Cross-platform build script for DeskMate
# Usage: ./build.sh [windows|macos|linux|all]
# 使用方法: ./build.sh [windows|macos|linux|all]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION="1.0.0"
APP_NAME="DeskMate"
BUILD_DIR="release"

# 颜色输出 / Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检测操作系统 / Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux";;
        Darwin*)    echo "macos";;
        CYGWIN*|MINGW*|MSYS*) echo "windows";;
        *)          echo "unknown";;
    esac
}

# 安装依赖 / Install dependencies
install_deps() {
    info "安装依赖 / Installing dependencies..."
    pip install -r requirements.txt
    pip install pyinstaller
}

# Linux 打包 / Linux build
build_linux() {
    info "构建 Linux 版本 / Building Linux version..."
    pyinstaller \
        --name "${APP_NAME}" \
        --windowed \
        --onefile \
        --clean \
        --noconfirm \
        --add-data "deskmate:deskmate" \
        --hidden-import="PyQt5" \
        --distpath "${BUILD_DIR}/linux" \
        --workpath "${BUILD_DIR}/build-linux" \
        deskmate/main.py

    # 重命名带版本号 / Rename with version
    mv "${BUILD_DIR}/linux/${APP_NAME}" "${BUILD_DIR}/linux/${APP_NAME}-${VERSION}-linux-x86_64"
    chmod +x "${BUILD_DIR}/linux/${APP_NAME}-${VERSION}-linux-x86_64"

    # 生成校验和 / Generate checksum
    cd "${BUILD_DIR}/linux" && sha256sum "${APP_NAME}-${VERSION}-linux-x86_64" > "${APP_NAME}-${VERSION}-linux-x86_64.sha256" && cd ../..

    info "Linux 构建完成 / Linux build complete: ${BUILD_DIR}/linux/"
}

# macOS 打包 / macOS build
build_macos() {
    info "构建 macOS 版本 / Building macOS version..."
    pyinstaller \
        --name "${APP_NAME}" \
        --windowed \
        --onefile \
        --clean \
        --noconfirm \
        --add-data "deskmate:deskmate" \
        --hidden-import="PyQt5" \
        --distpath "${BUILD_DIR}/macos" \
        --workpath "${BUILD_DIR}/build-macos" \
        --osx-bundle-identifier "com.deskmate.app" \
        deskmate/main.py

    mv "${BUILD_DIR}/macos/${APP_NAME}" "${BUILD_DIR}/macos/${APP_NAME}-${VERSION}-macos"
    chmod +x "${BUILD_DIR}/macos/${APP_NAME}-${VERSION}-macos"

    cd "${BUILD_DIR}/macos" && shasum -a 256 "${APP_NAME}-${VERSION}-macos" > "${APP_NAME}-${VERSION}-macos.sha256" && cd ../..

    info "macOS 构建完成 / macOS build complete: ${BUILD_DIR}/macos/"
}

# Windows 打包 / Windows build
build_windows() {
    info "构建 Windows 版本 / Building Windows version..."
    pyinstaller \
        --name "${APP_NAME}" \
        --windowed \
        --onefile \
        --clean \
        --noconfirm \
        --add-data "deskmate;deskmate" \
        --hidden-import="PyQt5" \
        --distpath "${BUILD_DIR}/windows" \
        --workpath "${BUILD_DIR}/build-windows" \
        deskmate/main.py

    mv "${BUILD_DIR}/windows/${APP_NAME}.exe" "${BUILD_DIR}/windows/${APP_NAME}-${VERSION}-windows-x86_64.exe"

    cd "${BUILD_DIR}/windows" && sha256sum "${APP_NAME}-${VERSION}-windows-x86_64.exe" > "${APP_NAME}-${VERSION}-windows-x86_64.exe.sha256" && cd ../..

    info "Windows 构建完成 / Windows build complete: ${BUILD_DIR}/windows/"
}

# 主流程 / Main
main() {
    local target="${1:-auto}"
    local os=$(detect_os)

    info "DeskMate v${VERSION} 打包工具 / Build tool"
    info "当前操作系统 / Current OS: ${os}"
    info "目标平台 / Target: ${target}"

    mkdir -p "${BUILD_DIR}"

    if [ "$target" = "auto" ]; then
        target="$os"
    fi

    case "$target" in
        linux)
            install_deps
            build_linux
            ;;
        macos)
            install_deps
            build_macos
            ;;
        windows)
            install_deps
            build_windows
            ;;
        all)
            install_deps
            warn "全平台打包建议在对应系统上分别执行 / Cross-platform builds should be done on each respective OS"
            build_linux
            ;;
        *)
            error "不支持的目标平台 / Unsupported target: $target"
            echo "用法 / Usage: $0 [linux|macos|windows|all]"
            exit 1
            ;;
    esac

    info "打包完成！产物位于 / Build complete! Artifacts in: ${BUILD_DIR}/"
    ls -la "${BUILD_DIR}/"*/ 2>/dev/null || true
}

main "$@"
