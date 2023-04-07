# dual_flir_cam_sync
Demo for dual camera capturing image under master-slave working mode, after loading predefine setting file of master and salve camera.

Hardwere and camera setting preparation/setup must done by connecting gpio cable with resister 1k om btw master and slave camera, for detailed operation setup can
reference the [Tutorial video](https://www.bilibili.com/video/BV1wG4y1z732/?share_source=copy_web&vd_source=352d0acd9feed0c12b01fd7848b932d3).

You should set up the virtual runtime enviorment and install flir spinnaker SDK in it with following README instruction in SDK package.

Setup virtual env as follow commands:

`conda create --name dual_flir_cam_syn python=3.8`

`conda activate dual_flir_cam_syn`

Use conda install tool under virtual env to install dependencies:

`conda install -c anaconda tk`

`conda install -c conda-forge opencv`

`conda install -c anaconda pillow`



