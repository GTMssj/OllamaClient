import json, requests, threading, os

class client():

    msgs = []
    model = ""
    host = ""

    def __init__(self):
        self.model = "dolphin-phi"
        self.host = "http://10.0.0.4:11434/api/chat"

    def get_input(self):
        inp = input("  > ")
        if inp[0] == '/':
            exit()
        else:
            self.msgs.append({
                                "role": "user", 
                                "content": inp
                            })

    def chat(self):
        r = requests.post(
                self.host, 
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
                #print(content, end = "")
                #print(content, end="", flush=True)
            if body.get("done", False):
                message["content"] = output
        self.msgs.append({
                            "role": "assistant", 
                            "content": output
                        })
        self.draw()
    
    def draw(self):
        os.system("clear")
        print(f"\n========================================\n")
        for line in self.msgs:
            print(f"{line['role']}: {line['content']}\n")
        print(f"\n========================================\n")

def main():
    cli = client()

    while True:
        cli.get_input()
        cli.chat()


if __name__ == "__main__":
    main()
