from flask import Flask, render_template, request, redirect, url_for
from models import db, Event
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

priority_order = {'High': 3, 'Medium': 2, 'Low': 1}

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

def format_time(time_obj):
    return time_obj.strftime("%H:%M")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        priority = request.form["priority"]

        new_start = parse_time(start_time)
        new_end = parse_time(end_time)

        existing_events = Event.query.filter_by(date=date).order_by(Event.start_time).all()

        for event in existing_events:
            event_start = parse_time(event.start_time)
            event_end = parse_time(event.end_time)

            overlaps = max(new_start, event_start) < min(new_end, event_end)
            if overlaps:
                if priority_order[priority] > priority_order[event.priority]:
                    # New event higher priority -> shift existing event forward
                    duration = event_end - event_start
                    event.start_time = format_time(new_end)
                    event.end_time = format_time(new_end + duration)
                    db.session.commit()
                else:
                    # New event lower or equal priority -> shift new forward
                    duration = new_end - new_start
                    new_start = event_end
                    new_end = new_start + duration

        updated_event = Event(
            name=name,
            date=date,
            start_time=format_time(new_start),
            end_time=format_time(new_end),
            priority=priority
        )
        db.session.add(updated_event)
        db.session.commit()
        return redirect(url_for("index"))

    events = Event.query.order_by(Event.date, Event.start_time).all()
    return render_template("index.html", events=events)

@app.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
