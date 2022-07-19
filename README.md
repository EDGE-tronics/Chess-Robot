<p align="center">
  <img src="https://github.com/Robotics-Technology/Chess-Robot/blob/master/interface_images/lss_arm_cb.png" width="400px"/>
</p>

# LSS Chess Robot

The LSS Chess Robot is a robotic arm that can play chess against you. This is a free and open source project that integrates aspects of robotics, computer vision, and of course chess.

## Table of Contents

- [Requirements](#requirements)
- [Modules list](#modules-list)
- [Getting Started](#getting-started)
- [Install](#install)
- [Run](#run)
- [Authors](#authors)
- [License](#license)
- [Resources](#resources)

## Requirements

### Hardware

- Lynxmotion Smart Servo (LSS) 4 DoF Robotic Arm
- Raspberry Pi or Windows PC
- Display
- Keyboard 
- Mouse
- Camera (USB or Raspberry Pi Camera Module)
- Lighting
- Chess board and pieces
- Speaker or Headphones (Optional)

### Software

- [OpenCV](https://opencv.org/)
- [Stockfish](https://stockfishchess.org/)
- [Python Chess](https://python-chess.readthedocs.io/en/latest/)
- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)

## Modules list

- [Vision Module](https://github.com/Robotics-Technology/Chess-Robot/VisionModule.py)
- [Chess Logic](https://github.com/Robotics-Technology/Chess-Robot/ChessLogic.py)
- [Arm Control](https://github.com/Robotics-Technology/Chess-Robot/ArmControl.py)
- [Interface](https://github.com/Robotics-Technology/Chess-Robot/Interface.py)

## Getting Started

To start using this project, proceed to the standard *clone* procedure:

```bash
cd <some_directory>
git clone https://github.com/Robotics-Technology/Chess-Robot.git
```

## Install

- On Windows PC

```
pip install -r requirements.txt
```
- On Raspberry Pi

```
pip3 install -r requirements.txt
pip3 install "picamera[array]"
```

If you have issues with OpenCV on the Raspberry Pi try the following commands:

```
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
sudo apt-get install libhdf5-dev 
sudo apt-get install libhdf5-serial-dev
sudo apt-get install python3-pyqt5
sudo apt-get install stockfish
sudo pip3 install opencv-python==3.4.6.27
sudo pip3 install opencv-contrib-python==3.4.6.27
```

## Run

```
cd <project_directory>
python Interface.py
```

<p align="center">
  <img src="https://github.com/Robotics-Technology/Chess-Robot/blob/master/interface_images/game_start.png" width="600px"/>
</p>
<p align="center">
  <img src="https://github.com/Robotics-Technology/Chess-Robot/blob/master/interface_images/lss_arm_setup.jpg" width="600px"/>
</p>
<iframe width="560" height="315" src="https://www.youtube.com/embed/Zy_o8n1uDR8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Authors

- [Geraldine Barreto](http://github.com/geraldinebc)
- [Eduardo Nunes](https://github.com/EduardoFNA)

## License

LSS Chess Robot is available under the GNU General Public License v3.0

## Contributing

Anyone is very welcome to contribute. Below is a list of identified improvements.

## To do

- Change  the gripper aperture acording to the chess piecce type
- Allow re-taking pictures in the case of board obstruction

## Limitations

- The chessboard is limited by the reach of the arm and the squares need to be big enough so the arm gripper doesn’t stumble upon adjacent pieces.
- This project was specifically made to be used with LSS smart servo motors using the LSS serial communication protocol so if you want to use it for a different robotic arm you will need to change how the servos are controlled and change the inverse kinematics parameters to match your specific arm.

## Resources

Every module of the project is explained in the tutorial series available [here](https://www.robotshop.com/community/robots/show/chess-playing-robot/).

Read more about the LSS Robotic Arm in the [wiki](https://www.robotshop.com/info/wiki/lynxmotion/view/servo-erector-set-robots-kits/ses-v2-robots/ses-v2-arms/lss-4dof-arm/).

Purchase the LSS arm on [RobotShop](https://www.robotshop.com/en/lynxmotion-smart-servos-articulated-arm.html).

Official Lynxmotion Smart Servo (LSS) libraries for Python available [here](https://github.com/Lynxmotion/LSS_Library_Python).

If you want more details about the LSS protocol, go [here](https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/).

Have any questions? Ask them on the Robotshop [Community](https://www.robotshop.com/community/).
