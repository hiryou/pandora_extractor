#!/bin/bash

chmod -R 775 PandoraExtractor
chmod -R 775 MY_MUSIC
chmod -R 775 README
echo "Setup files permission... Done"

chmod +x PandoraExtractor
echo "Setup executable... Done"

read -p "Press any key to finish..."
