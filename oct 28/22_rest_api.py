from flask import Flask, request, abort

app = Flask(__name__)

all_notes = {}

@app.route("/notes",methods=['POST'])
def create_note():
    text = request.json.get("text",None)
    all_keys = all_notes.keys()
    max_id = 1
    if(all_keys):
        max_id = max(all_keys)+1
    if text:
        all_notes[max_id] = text
        return {"id": max_id, "text": text}, 201
    else:
        abort(400)
@app.route("/notes",methods=['GET'])
def get_notes():
    return [{"id": note_id, "text": text} for note_id, text in all_notes.items()]

@app.route("/notes/<int:note_id>",methods=['GET'])
def get_one_note(note_id):
    if note_id in all_notes:
        return {"id": note_id, "text": all_notes[note_id]}
    else:
        abort(404)

@app.route("/notes/<int:note_id>",methods=['DELETE'])
def delete_one_note(note_id):
    if note_id in all_notes:
        del all_notes[note_id]
        return "Complete delete", 204
    else:
        abort(404)