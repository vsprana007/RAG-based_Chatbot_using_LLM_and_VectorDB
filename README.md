a. run mistral on ubuntu in windows 10/11:
    1. install ubuntu on wsl2 in windows
    2. run ubuntu 
    3. install ollama in ubuntu terminal using command: "curl -fsSL https://ollama.com/install.sh | sh"
    4. execute command to run mistral in ubuntu terminal: "ollama run mistral"

b. setup environment 
    1. open cmd in the project directory
    2. run command :"$ conda create --name <env> --file <requirements.txt>"

                OR

    1. open cmd in the project directory          
    2. create conda environment
    3. activate conda environment 
    4. install requiremnts.txt usnig : "conda install --file requirements.txt"

c. run project
    1. activate conda environment
    2. to run the project execute command: "streamlit run main.py"