# ./filter_questions_assistant_actions.py

import logging

class FilterQuestionsAssistantActions:
    
    def handle_actions(self, user_input):
        """
        Handles specific actions based on the user input for FilterQuestionsAssistant.
        """
        logging.info('Handling action for user input: %s', user_input)
        
        if user_input.lower() == 'show filter options':
            logging.info('Action: show filter options')
            return self.get_filter_options()
        
        if user_input.lower() == 'apply filter':
            logging.info('Action: apply filter')
            return 'Applying filter to questions based on your criteria.'
        
        if user_input.lower() == 'reset filter':
            logging.info('Action: reset filter')
            return 'Filters have been reset. Showing all questions.'
        
        return None

    def get_filter_options(self):
        """
        Returns the available filter options.
        """
        logging.info('Providing available filter options')
        return ('Filter options:\n'
                '1. By category\n'
                '2. By difficulty\n'
                '3. By date\n'
                '4. By relevance')

