#!/bin/bash

# STEP 1: Detect Ubuntu version to select ROS2 distro
UBUNTU_CODENAME=$(lsb_release -sc)
if [ "$UBUNTU_CODENAME" = "noble" ]; then
    ROS_DISTRO="jazzy"
else
    echo "ERROR: This script only supports Ubuntu 24.04 (noble) and ROS2 Jazzy."
    exit 1
fi
echo "Detected Ubuntu ($UBUNTU_CODENAME). Preparing to install ROS2 ($ROS_DISTRO)"

# STEP 2: Set of system locale
echo "Configuring system locale..."
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# STEP 3: Add ROS2 apt repository
echo "Adding ROS2 reposity keys and sources..."
sudo apt update && sudo apt install -y software-properties-common curl
sudo add-apt-repository universe
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

# STEP 4: Install ROS2 Packages
echo "Installing ROS2 base packages..."
sudo apt update
sudo apt upgrade -y
sudo apt install -y "ros-${ROS_DISTRO}-ros-base"

# STEP 5: Install ROS2 dev tools
echo "Installing ROS2 dev tools..."
sudo apt update && sudo apt install -y python3-rosdep ros-dev-tools
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    sudo rosdep init
fi
rosdep update

# STEP 6: Configure environment sourcing
BASHRC="$HOME/.bashrc"
SOURCE_CMD="source /opt/ros/${ROS_DISTRO}/setup.bash"
if ! grep -Fxq "$SOURCE_CMD" "$BASHRC"; then
    echo "Appending auto-source environment setup command to $BASHRC..."
    echo "" >> "$BASHRC"
    echo "# ROS 2 Environment Setup" >> "$BASHRC"
    echo "$SOURCE_CMD" >> "$BASHRC"
else
    echo "Auto-source command already present in $BASHRC."
fi

# Installation complete
echo "ROS2 ${ROS_DISTRO} installation completed successfully!"
