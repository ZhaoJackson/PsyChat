from transformers import AutoTokenizer, AutoModel


def get_dialogue_history(dialogue_history_list: list):
    dialogue_history_tmp = []
    for item in dialogue_history_list:
        if item['role'] == 'counselor':
            text = 'Counselor: ' + item['content']
        else:
            text = 'Visitor: ' + item['content']
        dialogue_history_tmp.append(text)

    dialogue_history = '\n'.join(dialogue_history_tmp)

    return dialogue_history + '\n' + 'Counselor: '


instruction = "Now you are playing the role of a professional psychological counselor. You have rich knowledge in psychology and mental health. You are skilled in using various psychological counseling techniques, " \
              "such as cognitive behavioral therapy principles, motivational interviewing techniques, and solution-focused brief therapy. With a warm and caring tone, show empathy and deep understanding of the visitor's " \
              "feelings. Engage in natural conversation with visitors, avoiding responses that are too long or too short, ensuring responses are smooth and human-like. " \
              "Provide deep guidance and insights, using specific psychological concepts and examples to help visitors explore their thoughts and feelings more deeply. Avoid didactic responses, " \
              "focusing more on empathy and respecting the visitor's feelings. Adjust responses based on visitor feedback to ensure responses fit the visitor's situation and needs."
# instruction = ''  #  <------ Uncomment to disable the above instruction


def get_instruction(dialogue_history):
    query = f'''
{instruction}
Dialogue:
{dialogue_history}'''

    return query


class PsyChatModel:
    def __init__(self):
        # Load model from local
        import torch
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained('PsyChat', trust_remote_code=True)
        self.model = AutoModel.from_pretrained('PsyChat', trust_remote_code=True)
        
        if self.device == 'cuda':
            self.model = self.model.cuda()
        
        self.model = self.model.eval()
        self.dialogue_history_list = []

    def new_line(self, usr_msg):
        # usr_msg = input('Visitor: ')
        if usr_msg == '0':
            exit()
        else:
            self.dialogue_history_list.append({
                'role': 'client',
                'content': usr_msg
            })
            dialogue_history = get_dialogue_history(dialogue_history_list=self.dialogue_history_list)
            query = get_instruction(dialogue_history=dialogue_history)
            response, history = self.model.chat(self.tokenizer, query, history=[], temperature=0.8, top_p=0.8)
            print(f'Counselor: {response}')
            self.dialogue_history_list.append({
                'role': 'counselor',
                'content': response
            })

            return response

    def new_line_with_history(self, history: str):
        assert not len(history.split('\n')) % 2
        history = history.replace('User:', 'Visitor: ')
        history = history.replace('Counselor:', 'Counselor: ')
        history = history.replace(' ', '')
        print(history)
        history += '\n' + 'Counselor: '
        query = get_instruction(dialogue_history=history)
        response, _ = self.model.chat(self.tokenizer, query, history=[], temperature=0.8, top_p=0.8)
        print(f'Counselor: {response}')

        return response
