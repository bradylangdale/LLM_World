class LLM:

    def __init__(self, client, style='chat', model_name=None, args={}, settings={}) -> None:
        self.client = client
        self.model_name = model_name
        self.args = args
        self.settings = settings
        self.style = style
        
        if not self.model_name is None:
            self.check_if_loaded()
        else:
            self.loaded = False

    def check_if_loaded(self):
        if self.client.get_model_info()['model_name'] != self.model_name:
            self.loaded = False
        else:
            self.loaded = True

        return self.loaded
    
    def inference(self, prompt, system=\
'''The following is a conversation with an AI Large Language Model.
The AI has been trained to answer questions, provide recommendations, and help with decision making.
The AI follows user requests. The AI thinks outside the box.\n'''):

        if not self.check_if_loaded():
            self.client.load_model({ 'model_name': self.model_name, 'args': self.args, 'settings': self.settings })

        prompt.append({ 'role': 'system', 'content': system })

        if self.style == 'chat':
            return self.client.chat_completion({
                'mode': 'instruct',
                "instruction_template": "Alpaca",
                'character': 'The Explorer',
                'messages': prompt,
                'temperature': 0.5,
                'max_tokens': 64,
                'stop': ['<\s>'],
            })['choices'][0]['message']['content']
        
        elif self.style == 'completion':
            return self.client.completion({ 'prompt': prompt, 'temperature': 0.001 })['choices'][0]['text']
        else:
            raise Exception('Invalid inferencing style.')