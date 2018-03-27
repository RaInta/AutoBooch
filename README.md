# AutoBooch
Description of my kombucha brewing system, automated using a Raspberry Pi

Tired of unpredictable brewing times for your kombucha? Worried about the health of your SCOBY*? 
Look no further! The AutoBooch is here! 

This is a system designed to maintain the temperature of your kombucha brewing system to a steady—and healthy—range, maximizing throughput and minimizing risk to your valuable SCOBY.




*This stands for **S**ymbiotic **C**ulture **O**f **B**acteria and **Y**east. It's a complicated matrix (or 'zoogleal mat') that is the brewing engine for the kombucha. The yeast forms a colony within a bacterial matrix that floats on top of the brew. The yeast consume the sugar in the raw brew (usually black tea and sugar), producing a small amount of ethanol. The bacteria consume the ethanol and some elements of the tea (including a reasonable fraction of the caffeine). The ethanol is oxidized, creating acetic ('vinegar') and other acids (gluconic, perhaps malic) may be formed in various concentrations, although concentrations of which are still debated.  



## Set as a cron job

    crontab -e

Given the heat capacity and expected temperature changes, sampling the temperature every half hour is easily adequate. So, set the cron job to: 

*/30 * * * * /absolute_path_to_your_script/brew_ctrl.py
