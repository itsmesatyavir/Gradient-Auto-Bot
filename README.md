# Gradient-Auto-Bot

This Python script uses Selenium to automate web interactions while rotating through a list of proxies to avoid detection and maintain a high level of anonymity. It uses a Chrome extension, downloads it if necessary, and attempts to connect to a web application using different proxies until a successful connection is made. Once a connection is established, it continues running tasks in the background with randomized delays between actions.

## Register Gradient

- Register Via Email : [*Gradient*](https://app.gradient.network/signup?code=N5CD2N)

## Join Us

[*MY CHANNEL*](https://t.me/AirdropInsiderID)

        █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
       ██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
       ███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
       ██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
       ██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║     
       ╚═╝  ╚═╝╚═╝╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                           
       ██╗███╗   ██╗███████╗██╗██████╗ ███████╗██████╗     
       ██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗    
       ██║██╔██╗ ██║███████╗██║██║  ██║█████╗  ██████╔╝    
       ██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗    
       ██║██║ ╚████║███████║██║██████╔╝███████╗██║  ██║    
       ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

## Features

- Rotates through multiple proxies from a `active_proxies.txt` file.
- Uses a Chrome extension (downloaded automatically) for enhanced functionality.
- Randomizes User-Agent headers to avoid detection.
- Runs tasks in parallel using `ThreadPoolExecutor` for concurrent proxy usage.
- Handles login to a web application and interacts with the UI.
- Random delays between actions to simulate human-like behavior.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.8 or higher
- Selenium
- WebDriver Manager
- Fake User-Agent Library
- .env file with the following environment variables:

  ```ini
  APP_USER=your_email@example.com
  APP_PASS=your_password

## Run

1. Clone Repository
  ```
  git clone https://github.com/airdropinsiders/Gradient-Auto-Bot.git && cd Gradient-Auto-Bot
  ```
2. Install Dependencies
  ```
  pip install -r requirements.txt
  ```
3. Run
  ```
  python3 bot.py
  ```
## Notes

- Proxy List: Ensure that active_proxies.txt contains a valid list of working proxies. If all proxies fail, the script will move to the next proxy.
- Extensions: The script automatically handles the download of a Chrome extension for enhanced functionality.
