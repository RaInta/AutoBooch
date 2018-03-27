# AutoBooch
Description of my kombucha brewing system, automated using a Raspberry Pi

Tired of unpredictable brewing times for your kombucha? Worried about the health of your SCOBY pellicle? Look no further! The AutoBooch has your back!

For context of what a SCOBY is, and some recipes and tricks, you should visit the Instructable associated with this project:
https://www.instructables.com/id/AutoBooch-Automate-Your-Kombucha-Brewing-System-Wi/


## Set as a cron job

    crontab -e

Given the heat capacity and expected temperature changes, sampling the temperature every half hour is easily adequate. So, set the cron job to: 

*/30 * * * * /absolute_path_to_your_script/brew_ctrl.py
