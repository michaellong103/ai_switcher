README.md
markdown
Copy code

# Assistant Router Application

## Overview

The Assistant Router Application is designed to route conversations to different assistant instances. This application includes a base assistant class, a factory to create specific assistants, and a router to handle conversation flow.

## Directory Structure

.
├── assistants
│ ├── init.py
│ ├── assistant_factory.py
│ ├── base_assistant.py
├── router
│ ├── init.py
│ ├── conversation_router.py
├── tests
│ ├── init.py
│ ├── test_router.py
│ ├── test_assistants.py
└── main.py

ruby
Copy code

## Files and Their Purpose

### `assistants/`

- **`__init__.py`**: Initialization file for the assistants module.
- **`assistant_factory.py`**: Contains the `ExampleAssistant` class and the `create_assistant` function.
- **`base_assistant.py`**: Defines the `BaseAssistant` abstract class which other assistants should inherit from.

### `router/`

- **`__init__.py`**: Initialization file for the router module.
- **`conversation_router.py`**: Contains the `ConversationRouter` class responsible for routing messages to the appropriate assistant.

### `tests/`

- **`__init__.py`**: Initialization file for the tests module.
- **`test_router.py`**: Unit tests for the `ConversationRouter` class using a mock assistant.
- **`test_assistants.py`**: Unit tests for the `BaseAssistant` class to ensure proper subclassing.

### `main.py`

Entry point of the application. It creates an example assistant and sets up the conversation router with it.

## Installation

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/assistant-router.git
cd assistant-router
Set up a virtual environment (optional but recommended):
sh
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:
Currently, there are no external dependencies. However, if dependencies are added later, you can install them using:

sh
Copy code
pip install -r requirements.txt
Usage
Run the application using:

sh
Copy code
python main.py
This will create an example assistant and set up a conversation router with it. The router will then route a sample message to the assistant.

Running Tests
To run the unit tests, use:

sh
Copy code
python -m unittest discover tests
This will discover and run all tests in the tests directory.

Extending the Application
Adding a New Assistant
Create a new assistant class:
python
Copy code
# assistants/new_assistant.py
from .base_assistant import BaseAssistant

class NewAssistant(BaseAssistant):
    def respond(self, message):
        return 'new assistant response'
Register the new assistant in the factory:
python
Copy code
# assistants/assistant_factory.py
from .new_assistant import NewAssistant

def create_assistant(assistant_type):
    if assistant_type == 'example':
        return ExampleAssistant()
    elif assistant_type == 'new':
        return NewAssistant()
    else:
        raise ValueError('Unknown assistant type')
Update the main entry point if necessary:
python
Copy code
# main.py
from assistants.assistant_factory import create_assistant
from router.conversation_router import ConversationRouter

def main():
    example_assistant = create_assistant('example')
    new_assistant = create_assistant('new')
    router = ConversationRouter([example_assistant, new_assistant])
    print(router.route('Hello'))

if __name__ == '__main__':
    main()
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please create a pull request or submit an issue to discuss changes.

Contact
For any questions or feedback, please contact [your email address].

vbnet
Copy code
