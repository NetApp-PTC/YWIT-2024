# YWIT-2024
The NetApp PTC Young Women in Technology conference for 2024

## Workshops

### MicroPython on Microcontrollers
This workshop will introduce the student to Python coding, electronics, and project
design. We will building several projects ranging from simple to complicated. These
projects are based on the ESP32-C3 microcontroller which is running MicroPython and
they depend on some other electronics components such as LEDs, buttons, and more.
See the project guide for step by step instructions on each project as well as mini
tutorials for electronics and programming beginners.

You can view the project guide [here](https://netapp-ptc.github.io/YWIT-2024/project_guide.pdf)

#### Building the Guide PDF
If you want to edit and build the guide locally, the easiest way is to use docker to
run the TeX Live image. One way to do this is to install the LaTeX Workshop plugin for
VSCode (https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) and
then set the settings `latex-workshop.docker.enabled: true` and
`latex-workshop.docker.image.latex: "registry.gitlab.com/islandoftex/images/texlive:latest"`.
Once you do this and open a .tex file (any of them), there will be a green play button in
the top right of the editor. The first time it will download the docker image and then build
it (takes a few minutes). Subsequent builds are pretty fast.

#### Flashing the Microcontroller Image
If you want to flash a microcontroller with the exact version of all of the software that was used
here, you can use [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32c3/esptool/index.html)
to do so. Just connect your microcontroller and run `esptool.py --chip esp32c3 --port <port> write_flash 0 micropython_workshop/microcontroller_image.bin`.
Make sure you fill in `<port>` with the relevant port your computer assigns it.
