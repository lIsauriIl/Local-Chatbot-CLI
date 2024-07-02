# Local-Chatbot-CLI
Hi there! I made a chatbot interface that allows you to do some basic customisation of the chatbot before starting the session. These customisations include adding a system prompt, which is basically the same thing as telling your chatbot what it needs to do or help you do, as well as selection of the chatbot model. I made the chatbot CLI using LangChain and Ollama.

# Installation and setup
First, navigate to your desired folder on your command line of choice and copy this code:

```git clone https://github.com/lIsauriIl/Local-Chatbot-CLI.git```

After that, run this command:

```pip install -r requirements.txt```

# Usage
There's nothing much you need to do other than to run the file. However, if you want to install a model from Ollama, you have to browse the Ollama documentation to see which model you want to install. From there, there are 2 options: either install the model yourself via the command:

```ollama pull [model_name]```

Or attempt to run chatbot using the model that you haven't installed yet. If that happens, you will get as far as being able to ask a question. However, instead of giving an answer, the interface will ask you if you want to download the model, since it doesn't exist yet.

There's nothing else to keep in mind that isn't explained in the CLI itself.
