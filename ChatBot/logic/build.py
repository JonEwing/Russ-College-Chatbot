from chatterbot.trainers import ChatterBotCorpusTrainer
from tools import chatbot_logger
from chatterbot import ChatBot
import chatterbot.response_selection
import chatterbot.comparisons

build_log = chatbot_logger.BuildLogger('build.log')
logger = build_log.logger

'''Chatbot default response when the confidence of any
response is below the threshhold (confidence_lower_bound)
'''
default_response = 'I do not understand your question.' \
                    ' Could you try rephrasing it?' \
                    ' Or type "help with bot" for more information.' \

logger.info("Set default response: {}".format(default_response))

confidence_lower_bound = 0.5
logger.info("Set Chatterbot confidence lower-bound: {}".format(confidence_lower_bound))

'''Chatterbot response selection methods: `get_random_response`
'''
response_selection_ = chatterbot.response_selection.get_random_response
logger.info("Set default response selector: {}".format(response_selection_))

'''Chatterbot statement comparison methods: `levenshtein_distance`
'''
comparison_ = chatterbot.comparisons.levenshtein_distance
logger.info("Set default comparison method: {}".format(comparison_))

'''Chatterbot statement preprocessors:
`clean_whitespace`
`unescape_html`
`convert_to_ascii`
'''
preprocessors_ = [
    "chatterbot.preprocessors.clean_whitespace",
    "chatterbot.preprocessors.unescape_html",
    "chatterbot.preprocessors.convert_to_ascii"
]
logger.info("Set default preprocessor(s): {}".format(preprocessors_))

'''Chatterbot logic adapters and user-defined
logic adapters to supply non-trained responses:
`BestMatch`
`WikiLogicAdapter`
`WeatherAdapter`
'''
logic_adapters_ = [
    {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': default_response,
        'maximum_similarity_threshold': confidence_lower_bound
    },
    {'import_path': 'logic.logic_adapters.wiki_adapter.WikiLogicAdapter'},
    {'import_path': 'logic.logic_adapters.weather_adapter.WeatherAdapter'},
    {'import_path': 'logic.logic_adapters.tour_adapter.TourAdapter'},
]
logger.info("Set default logic adapter(s): {}".format(logic_adapters_))

'''
#################################################
'''

'''Build R2
'''
name = 'R2'
logger.info("Building Chatterbot.Chatbot: {}".format(name))
chatbot = ChatBot(name,
            response_selection_method=response_selection_,
            statement_comparison_function=comparison_,
            preprocessors=preprocessors_,
            logic_adapters=logic_adapters_,
            read_only=True)

'''Create a new trainer for R2
'''
logger.info("Building ChatterbotCorpusTrainer")
trainer = ChatterBotCorpusTrainer(chatbot)

'''Train R2 on `responses` folder
'''
logger.info("Starting Training")

trainer.train("responses")
logger.info("Ended Training")
    