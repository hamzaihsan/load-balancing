import traceback
from flask import Flask, render_template
from flask import request


class ML:
    def __init__(self):
        self.mod = []
        self.avaliable_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.loaded_models_limit = 2
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.avaliable_models)[:self.loaded_models_limit]
        }

    def load_weights(self, model):
        return self.avaliable_models.get(model, None)

    def mini(self):
        min_model = next(iter(self.loaded_models))
        second = next(iter(self.loaded_models))
        if self.mod.count(min_model) > self.mod.count(second):
            min_model = second
        return min_model

    def max(self):
        max_model = next(iter(self.avaliable_models))
        for v in self.mod:
            if self.mod.count(max_model) < self.mod.count(v):
                max_model = v
        return max_model

    def give_model(self, new_model):
        if new_model in self.avaliable_models:
            return new_model

    def load_balancer(self, new_model):
        if not len(self.mod):
            self.loaded_models.pop(next(iter(self.loaded_models)))
            if self.give_model(new_model):
                new = self.give_model(new_model)
                str1 = "/additional_drive/ML/"
                str2 = str1 + new
                self.loaded_models[new] = str2
        else:
            self.loaded_models.pop(self.mini())
            str1 = "/additional_drive/ML/"
            str2 = str1 + str(self.max())
            self.loaded_models[self.max()] = str2
        print(self.loaded_models)


app = Flask(__name__)
ml = ML()


@app.route('/get_loaded_models', methods=['GET', 'POST'])
def get_loaded_models():
    return ml.loaded_models


@app.route('/')
def load():
    return render_template("input.html")


@app.route('/process_request', methods=['GET', 'POST'])
def process_request():
    try:
        model = request.form["model"]
        if model not in ml.loaded_models:
            ml.load_balancer(model)
        ml.mod.append(model)
        return "processed by " + ml.loaded_models[model]
    except:
        return str(traceback.format_exc())


app.run(host='0.0.0.0', port=5000)
