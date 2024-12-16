# Sample Lock

## Description
The Sample-Lock is an advanced software application designed to provide a graphical user interface (GUI) for the Sample-lock protocol, a microscopy image stabilization technique. This system integrates hardware control and data processing functionalities, offering a robust solution for researchers requiring precise image stabilization in microscopic studies.

## Visuals
![System Screenshot](pics/GUI_new.png)
This screenshot displays the Sample-Lock software interface, specifically designed for microscopy image stabilization. The main panel presents a high-resolution image of a sample being examined. Below this, two graphs offer real-time monitoring of 3-axis stabilization data: the upper graph displays the position of the piezo stage along a single axis (blue line), and the lower graph illustrates the computed discrepancies between actual and desired movements along that axis (red line). To the right, the control panel contains settings for the sample-lock protocol, alongside options to save data and adjust operational settings. The interface also features tabs for managing both coarse (motor stage) and precise (piezo stage) movements, with an additional tab dedicated to camera settings.

## Prerequisites

Before installing, ensure you have the following prerequisites installed:
- Python 3.9 or higher
- Camera Drivers:
    -   Andor Camera Drivers: Required for operating Andor cameras. Available through [Andor's website](https://andor.oxinst.com/products/).
    -   IDS Camera Drivers: Necessary for integrating IDS cameras. Download from [IDS's official site](https://en.ids-imaging.com/).
- Stage Drivers:
    - Thorlabs Drivers: For controlling Thorlabs stages, install the appropriate drivers from Thorlabs' support page.
    - PI Drivers: Access the drivers at PI's download section.

## Installation

To get started with this project, clone the repository and install the required dependencies:

```bash
git clone git@github.com:jvorlauf/Sample-lock.git
cd Sample-lock
pip install -r requirements.txt
```

## Features
- Multiple Camera Support: Compatible with various camera models and can be easily extended.
- Stage Control: Fine and coarse control of motorized stages with precision settings.
- Real-time Data Processing: Live data visualization and error handling for real-time performance monitoring.
- Extensive Configuration: Easy to configure system parameters through a GUI interface or configuration files.

## Contributing
Interested in contributing? Great! Please check out our contributing guidelines for ways to offer feedback and contribute.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.