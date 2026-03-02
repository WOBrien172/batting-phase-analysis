balls_faced = 0
total_score = 0
dot_streak = 0
dot_streak_runs = 0
dot_streak_balls = 0
last_six_balls_score = 0
scoring_values = {0:0, 1:0, 2:0, 3:0, 4:0, 6:0}
last_ball = None
labels = {
    0: "dots",
    1: "singles",
    2: "twos",
    3: "threes",
    4: "fours",
    6: "sixes"
}
after_event = {
    0: {"runs":0, "balls":0, "boundaries":0},
    1: {"runs":0, "balls":0, "boundaries":0},
    2: {"runs":0, "balls":0, "boundaries":0},
    3: {"runs":0, "balls":0, "boundaries":0},
    4: {"runs":0, "balls":0, "boundaries":0},
    6: {"runs":0, "balls":0, "boundaries":0}
}
ball_position = {
    1: {"runs":0, "balls":0, "boundaries":0},
    2: {"runs":0, "balls":0, "boundaries":0},
    3: {"runs":0, "balls":0, "boundaries":0},
    4: {"runs":0, "balls":0, "boundaries":0},
    5: {"runs":0, "balls":0, "boundaries":0},
    6: {"runs":0, "balls":0, "boundaries":0}
}
phases = {
    "early_powerplay": {"runs":0, "balls":0, "boundaries":0},
    "late_powerplay": {"runs":0, "balls":0, "boundaries":0},
    "early_middle": {"runs":0, "balls":0, "boundaries":0},
    "middle_middle": {"runs":0, "balls":0, "boundaries":0},
    "late_middle": {"runs":0, "balls": 0, "boundaries":0},
    "death": {"runs":0, "balls":0, "boundaries":0}
}
final_ball = 0
last_three_balls_score = 0
six_ball_segments = []
boundary_balls = []
afterevent_output_list = []
ballno_output_list = []
phases_output_list = []

def get_number(prompt, minimum, maximum):
    while True:
        try:
            variable = int(input(prompt))
        except ValueError:
            print("Invalid input. Enter a valid number.")
            continue

        if variable < minimum or variable > maximum:
            print("Invalid input. Enter a valid number.")
            continue

        return variable
    
def get_phases(x):
    if x == 20:
        return 3, 6, 9, 13, 16
    elif x == 25:
        return 4, 7, 11, 16, 20
    elif x == 30:
        return 4, 8, 12, 18, 24
    elif x == 35:
        return 4, 8, 15, 22, 28
    elif x == 40:
        return 4, 8, 17, 26, 34
    elif x == 45:
        return 4, 9, 18, 30, 37
    elif x == 50:
        return 5, 10, 20, 30, 40
    

match_overs = get_number("How many overs per innings per side?", 20, 50)
early_powerplay, late_powerplay, early_middle, middle_middle, late_middle = get_phases(match_overs)
if_out = str(input("Did they get out? (Y/N)").lower())
while if_out not in ["y", "n"]:
    if_out = str(input("Did they get out? (Y/N)").lower())
total_balls_faced = get_number("How long was total innings (balls)?", 0, 300)
over_in = get_number("Which over (no.) did they come in?", 1, match_overs)
over_out = get_number("Which over (no.) did they face their last ball?", over_in, match_overs)

for i in range((over_out-over_in+1)):
    ball_in_over = 0
    over_string = input("Enter over string (use '/' if batter did not face ball), for example, (1/3//6). " \
    "If player went in during over, signal with '/' for balls not faced by batter." \
    "Use '0' for wicket ball.")
    for char in over_string:
        ball_in_over = ball_in_over + 1
        if char == '/':     # Batter did not face this ball
            continue
        else:
            event = int(char)
            over = over_in + i
            if i == total_balls_faced-1:
                final_ball = last_ball
            if balls_faced+4 >= total_balls_faced and balls_faced+1 != total_balls_faced:
                last_three_balls_score += event
            total_score = total_score + event
            last_six_balls_score = last_six_balls_score + event
            balls_faced = balls_faced + 1
            if over <= early_powerplay:
                phase = "early_powerplay"
            elif over <= late_powerplay: 
                phase = "late_powerplay"
            elif over <= early_middle:
                phase = "early_middle"
            elif over <= middle_middle:
                phase = "middle_middle"
            elif over <= late_middle:
                phase = "late_middle"
            else:
                phase = "death"
            phases[phase]["runs"] += event
            phases[phase]["balls"] += 1
            if event >= 4:
                phases[phase]["boundaries"] += 1
            if last_ball != None:
                after_event[last_ball]["runs"] += event
                after_event[last_ball]["balls"] += 1
                if event >= 4:
                    after_event[last_ball]["boundaries"] += 1
            scoring_values[event] += 1
            if event in [4,6]:
                boundary_balls.append(balls_faced)
            if dot_streak >= 3:
                dot_streak_runs = dot_streak_runs + event
                dot_streak_balls = dot_streak_balls + 1
            if event == 0:
                dot_streak = dot_streak + 1
            else:
                dot_streak = 0
            print(f"{total_score} ({balls_faced})")
            if balls_faced % 6 == 0:
                six_ball_segments.append(last_six_balls_score)
                last_six_balls_score = 0
            if if_out == "y":
                if balls_faced + 1 == total_balls_faced:
                    final_ball = event
            ball_position[ball_in_over]["runs"] += event
            ball_position[ball_in_over]["balls"] += 1
            if event >= 4:
                ball_position[ball_in_over]["boundaries"] += 1
            last_ball = event
    print(f"End of over {over_in + i}")

phase_ranges = [
    ("Early Powerplay", 1, early_powerplay),
    ("Late Powerplay", early_powerplay + 1, late_powerplay),
    ("Early Middle", late_powerplay + 1, early_middle),
    ("Middle Overs", early_middle + 1, middle_middle),
    ("Late Middle Overs", middle_middle + 1, late_middle),
    ("Death Overs", late_middle + 1, match_overs)
]

phase_keys = [
    "early_powerplay",
    "late_powerplay",
    "early_middle",
    "middle_middle",
    "late_middle",
    "death"
]

print("---INNINGS SUMMARY---")
if if_out == "n":
    print(f"{total_score}* ({total_balls_faced})")
else:
    print(f"{total_score} ({total_balls_faced})")
print(f"Runs per 6 ball segments: {six_ball_segments}")
print(f"{scoring_values[0]} dots")
print(f"{scoring_values[1]} singles")
print(f"{scoring_values[2]} twos")
print(f"{scoring_values[3]} threes")
print(f"Boundary Balls: {boundary_balls}")
if if_out == "y":
    print(f"Total from last three balls before dismissal: {last_three_balls_score}")
for key in after_event:
    runs = after_event[key]["runs"]
    balls = after_event[key]["balls"]
    boundaries = after_event[key]["boundaries"]

    print(f"Ball after {labels[key]}: {runs} off {balls} with {boundaries} boundaries.")

for i in range(len(phase_keys)):
    name, start, end = phase_ranges[i]
    key = phase_keys[i]
    
    runs = phases[key]["runs"]
    balls = phases[key]["balls"]
    boundaries = phases[key]["boundaries"]
    
    print(f"{name} (overs {start}-{end}): {runs} off {balls} with {boundaries} boundaries.")

for i in range(1, 7):
    runs = ball_position[i]["runs"]
    balls = ball_position[i]["balls"]
    boundaries = ball_position[i]["boundaries"]
    print(f"Ball {i} in Over: {runs} off {balls} with {boundaries} boundaries")

print(f"After dot streaks (3+ dot balls): {dot_streak_runs} off {dot_streak_balls}")

print("---STATS FOR COPY/PASTE INTO SHEETS---")

print("Scoring Breakdown:," + ",".join(map(str,[scoring_values[k] for k in [0,1,2,3]])))

for key in [0,1,2,3,4,6]:
    afterevent_output_list.append(after_event[key]["runs"])
    afterevent_output_list.append(after_event[key]["balls"])
    afterevent_output_list.append(after_event[key]["boundaries"])
print("Leading from balls:," + ",".join(map(str, afterevent_output_list)))

print("Runs per 6 ball segment:," + ",".join(map(str,six_ball_segments)))

before_dismissal = [last_three_balls_score, final_ball]

if if_out == "y":
    print("Before dismissal stats:," + ",".join(map(str, before_dismissal)))

for key in ["early_powerplay","late_powerplay","early_middle","middle_middle","late_middle","death"]:
    phases_output_list.append(phases[key]["runs"])
    phases_output_list.append(phases[key]["balls"])
    phases_output_list.append(phases[key]["boundaries"])
print("Match Stage Breakdown:," + ",".join(map(str,phases_output_list)))

for pos in range(1,7):
    ballno_output_list.append(ball_position[pos]["runs"])
    ballno_output_list.append(ball_position[pos]["balls"])
    ballno_output_list.append(ball_position[pos]["boundaries"])

print("Ball in over breakdown:," + ",".join(map(str,ballno_output_list)))   

print(f"Boundary Balls: {boundary_balls}")

dot_stats = [dot_streak_runs, dot_streak_balls]

print("After dot streaks:," + ",".join(map(str, dot_stats)))
