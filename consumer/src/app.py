from flask import Flask, request
from event_stream import Stream
import json

app = Flask(__name__)
dispatcher = Stream(app.logger) #TODO: There's probably a better way to encapsulate logging

@app.route("/")
def index():
    return "This is the event generator.  To read an event from the stream issue a GET on the /events endpoint."

@app.route("/events", methods=['GET'])
def read_event():
    message = dispatcher.read_stream()
    app.logger.debug("Read this data from the stream: {0}".format(message))
    if message:
        return json.dumps(message), 200
    return json.dumps({'status': 'error', 'message': 'Unable to read from the message stream.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
