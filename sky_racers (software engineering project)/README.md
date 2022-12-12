# README #

Switch to the Cycle1 branch using git checkout Cycle1 for the cycle 1 deliverable

Switch to the Cycle2 branch using git checkout Cycle2 for the cycle 2 deliverable

Switch to the Cycle3 branch using git checkout Cycle3 for the cycle 3 deliverable

### What is this repository for? ###

* This is a racing game for our CS370 project
* Version 1.0

### How do I get set up? ###

BUILD INSTRUCTIONS:

Install python3
    sudo apt-get install python3

Install pip
    sudo apt-get install python3-pip

Install pygame, box2d, and pickle using pip
    pip install box2d-py
    pip install pygame
    pip install pickle_mixin

INSTALL INSTRUCTIONS:

Note: Sky Racers is installable on Linux and Windows
Windows install requires the sky racers repo to be contained in the user’s home directory

    run ./Install in the sky_racers directory to install sky_racers
    run ./Uninstall in the sky_racers directory to uninstall sky_racers

Create a 1024x768 map and name it map.png
Copy this map.png file to assets/boundary_editor and assets/game
Run edit_level_sky_racers to edit your map
Once you finish editing, save the file. You will now have a file named map.data in your main 
directory.
Copy this file to assets/game

Run sky_racers anywhere to play the game


TESTING:

    Run ./run_tests in the test directory to run all tests at once
    To run tests separately refer to the run_tests script
