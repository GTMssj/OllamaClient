import json, requests, threading, os

class client():

    msgs = []
    model = ""
    host = ""

    def __init__(self):
        self.model = "dolphin-phi"
        self.host = "http://52.229.187.190:11434/api"

    def get_input(self):
        try:
            inp = input("\n  > ")
        except KeyboardInterrupt:
            print("\n   Exiting...")
            exit()
        if not inp:
            exit()
        else:
            if inp[0] == '/':
                args = inp.split(" ")
                args[0] = args[0][1:]
                if args[0] == 'show' or args[0] == 'list':
                    r = requests.get(self.host + "/tags")
                    res = r.json()['models']
                    print("\nModels:")
                    print("--------------------------")
                    for line in res:
                        print(f"    {line['details']['parameter_size']}  {line['name'].split(':')[0]}")
                    print("--------------------------")
                if args[0] == 'set':
                    self.host = f"http://{args[1]}:{args[2]}/api"
                    self.draw()
                if args[0] == 'run':
                    self.model = args[1]
                    self.draw()
                if args[0] == 'help' or args[0] == '?':
                    self.help()
                if args[0] == 'exit' or args[0] == 'quit' or args[0] == 'q':
                    exit()
            else:
                self.msgs.append({
                                    "role": "user", 
                                    "content": inp
                                })
                self.chat()

    def chat(self):
        r = requests.post(
                self.host + "/chat", 
                json = {
                        "model": self.model, 
                        "messages": self.msgs, 
                        "stream": True
                    }
            )
        r.raise_for_status()
        output = ""
        print()
        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                output += content
            if body.get("done", False):
                message["content"] = output
        self.msgs.append({
                            "role": "assistant", 
                            "content": output
                        })
        self.draw()
    
    def draw(self):
        os.system("clear")
        print(f"\n========================================")
        print(f"  running: {self.model} on {self.host}")
        print(f"===============[History]================")
        for line in self.msgs:
            print(f"  | {line['role']}: {line['content']} |")
        print(f"========================================")
    
    def help(self):
        print(
                f"\n"+
                "Useage:\n\n"+
                "   [prompt]                to Chat\n\n"+
                "   /exit or /quit          to Exit program\n"+
                "   /set [addr] [port]      to Change settings\n"+
                "   /run [model]            to Change model to use\n"+
                "   /show                   to List Models can be used\n"+
                "   /help or /?             to Show this list of commands"
            )

def main():
    cli = client()
    cli.draw()
    cli.help()

    while True:
        cli.get_input()

if __name__ == "__main__":
    main()
