import boto3
ddb = boto3.client("dynamodb")
import ask_sdk_core
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response

sb = SkillBuilder()



class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        speech_text = "Welcome to Baby Bump! I'm Lisa. When was your last menstrual period?"
        return (
            handler_input.response_builder
                .speak(speech_text)
                .set_should_end_session(False)
                .response
        )


class ErrorHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speech_text = 'Sorry, your skill encountered an error';
        print(exception)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

        
class BabyBumpHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BabyBump")(handler_input)

    def handle(self, handler_input):
        date = handler_input.request_envelope.request.intent.slots['date'].value
        month = handler_input.request_envelope.request.intent.slots['month'].value
        year = handler_input.request_envelope.request.intent.slots['year'].value
        #weeks= calculator(date, month, year)
        speech_text = "Okay so your last period was on {month} {date} {year}".format(month=month, date=date, year=year);
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    #def calculator(date, month, year):




sb.add_exception_handler(ErrorHandler())

#delete undefined built-in intent handlers
sb.add_request_handler(LaunchRequestHandler())

#add custom request handlers
sb.add_request_handler(BabyBumpHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)
