from copy import deepcopy

from flask import Flask, jsonify, render_template, request
from src.config import call_audio
from src.ai_interaction import ai_request
import threading


def add_history_input(input_, role, current_key_):
    user_stories[str(current_key_)]["history"].append({"role": role, "content": input_})


stories = {
    "warrior": {
        "story": "The dragon has been terrorizing the countryside, its fiery breath leaving villages in ruins. The people have turned to you, their last hope, to slay the beast. Clad in armor, sword and shield in hand you go up the mountain to the Dragon's Lair. What will you do?",
        "context": " The user is very athletic and strong, but cannot use magic.",
    },
    "rogue": {
        "story": "The King's Crown sits atop a golden pedestal, locked away in a heavily guarded tower. It is said to be the key to a rebellion long overdue. You stand menacingly atop the king's castle, staring at the tower in the distance. What will you do?",
        "context": "The user is very stealthy, but weak and ugly.",
    },
    "paladin": {
        "story": "A sacred artifact has been stolen from the Church, and its absence has left the faithful in despair. The artifact lies in the clutches of a demon in the deepest crypt. You stand in the ruins of a desolate church, prepared to draw the sigil to enter the demon realm. What will you do?",
        "context": "The user can call the power of God, but vomits every time they act evil.",
    },
    "druid": {
        "story": "Deep in the forgotten jungle, a lost temple hides the spirits of the ancient guardians. You journey forward to awaken the spirits. The path is perilous, filled with traps and trials meant to test your worth. In front of you lies three doors. What will you do?",
        "context": "The user can shapeshift into animals, but is very dumb.",
    },
    "jeff": {
        "story": "You're lost in the middle of a cursed forest where the trees whisper secrets and the shadows hunt for flesh. The only goal is to see the sun again. You stand in a clearing, thinking of your next step. What will you do?",
        "context": "The user has a big heart but is very dumb and ugly, which is constantly brought up.",
    },
    "wizard": {
        "story": "A rival wizard has conjured storms and chaos across the land, threatening to engulf the world in shadow. You’ve tracked them to their ominous tower, but their magic is said to rival even the gods. What will you do?",
        "context": "The user can use magic, but is very unathletic.",
    },
}

history = [
    {
        "role": "system",
        "content": "You are a very descriptive narrator. Every input sent by the user is meant to move the story forward."
        "Random conflict will happen during the adventure. The answers must be only a paragraph long."
        "Dialogue may happen. The user's name is {{user}}. ",
    },
    {
        "role": "assistant",
        "content": "In the gray twilight of a rainy hill, Loric stood, his cloak blending with the stormy sky. Below, a quiet village glimmered with torchlight, a brief stop on his journey. Rumors of a powerful artifact at the Lost Keep called him onward. Clutching his staff, he descended, ready for what the night might bring.",
    },
]

user_stories = {}

app = Flask(__name__)


# Main page route
@app.route("/")
def main_page():
    return render_template("index.html")


# This function will be the one to provide the user's answer to the AI and give the UI a response.
@app.route("/get_data", methods=["GET"])
def get_data():
    user_input = request.args.get("name")
    current_key = request.args.get("story")
    if current_key not in user_stories.keys():
        aux_history = deepcopy(history)
        name = request.args.get("info").split("|")[0]
        classe = request.args.get("info").split("|")[1]
        user_stories[str(current_key)] = {"name": name, "history": aux_history}

        user_stories[str(current_key)]["history"][1]["content"] = "You are " + name + ". " + stories[classe]["story"]
        user_stories[str(current_key)]["history"][0]["content"] += stories[classe]["context"]
        user_stories[str(current_key)]["history"][0]["content"] = aux_history[0]["content"].replace("{{user}}", name)
        data = {"message": user_stories[str(current_key)]["history"][1]["content"], "status": "success"}
    else:
        add_history_input(user_input, "user", current_key)
        answer = ai_request(user_stories[str(current_key)]["history"])
        data = {"message": answer.content, "status": "success"}

        # threading.Thread(target=call_audio, args=(answer.content,)).start()
        # data = {'message': "haha", 'status': 'success'}

    print(user_stories.keys())
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
