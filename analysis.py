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
    0: {"runs":0, "balls":0},
    1: {"runs":0, "balls":0},
    2: {"runs":0, "balls":0},
    3: {"runs":0, "balls":0},
    4: {"runs":0, "balls":0},
    6: {"runs":0, "balls":0}
}
ball_position = {
    1: {"runs":0, "balls":0},
    2: {"runs":0, "balls":0},
    3: {"runs":0, "balls":0},
    4: {"runs":0, "balls":0},
    5: {"runs":0, "balls":0},
    6: {"runs":0, "balls":0}
}
phases = {
    "early_powerplay": {"runs":0, "balls":0},
    "late_powerplay": {"runs":0, "balls":0},
    "early_middle": {"runs":0, "balls":0},
    "middle_middle": {"runs":0, "balls":0},
    "late_middle": {"runs":0, "balls":0},
    "death": {"runs":0, "balls":0}
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

match_overs = get_number("How many overs per innings per side?", 20, 50)
if_out = str(input("Did they get out? (Y/N)").lower())
while if_out not in ["y", "n"]:
    if_out = str(input("Did they get out? (Y/N)").lower())
total_balls_faced = get_number("How long was total innings (balls)?", 0, 300)
over_in = get_number("Which over (no.) did they come in?", 1, format)
over_out = get_number("Which over (no.) did they face their last ball?", over_in, format)

if match_overs == 20:
    early_powerplay = 3
    late_powerplay = 6
    early_middle = 9
    middle_middle = 13
    late_middle = 16
elif match_overs == 30:
    early_powerplay = 4
    late_powerplay = 7
    early_middle = 12
    middle_middle = 18
    late_middle = 25
elif match_overs == 40:
    early_powerplay = 4
    late_powerplay = 8
    early_middle = 15
    middle_middle = 23
    late_middle = 32
elif match_overs == 50:
    early_powerplay = 5
    late_powerplay = 10
    early_middle = 20
    middle_middle = 30
    late_middle = 40
else:
    early_powerplay = match_overs // 6
    late_powerplay = match_overs // 3
    early_middle = match_overs // 2
    middle_middle = 2*match_overs // 3
    late_middle = match_overs - early_powerplay

for i in range((over_out-over_in+1)):
    ball_in_over = 0
    over_string = input("Enter over string (use '/' if batter did not face ball), for example, (1/3//6). If player went in during over, signal with '/' for balls not faced by batter.")
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
            if last_ball != None:
                after_event[last_ball]["runs"] += event
                after_event[last_ball]["balls"] += 1
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
            last_ball = event

phase_ranges = [
    ("Early Powerplay", 1, early_powerplay),
    ("Late Powerplay", early_powerplay + 1, late_powerplay),
    ("Early Middle", late_powerplay + 1, early_middle),
    ("Middle Overs", early_middle + 1, middle_middle),
    ("Late Middle Overs", middle_middle + 1, late_middle),
    ("Death Overs", late_middle + 1, format)
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
    print(f"Ball after {labels[key]}: {runs} off {balls}")
for i in range(len(phase_keys)):
    name, start, end = phase_ranges[i]
    key = phase_keys[i]
    
    runs = phases[key]["runs"]
    balls = phases[key]["balls"]
    
    print(f"{name} (overs {start}-{end}): {runs} off {balls}")
for i in range(1, 7):
    runs = ball_position[i]["runs"]
    balls = ball_position[i]["balls"]
    print(f"Ball {i} in Over: {runs} off {balls}")

print(f"After dot streaks (3+ dot balls): {dot_streak_runs} off {dot_streak_balls}")

print("---STATS FOR COPY/PASTE INTO SHEETS---")

print("Scoring breakdown:\t" + "\t".join(
    map(str, [scoring_values[k] for k in [0,1,2,3,4,6]])))

for key in [0,1,2,3,4,6]:
    afterevent_output_list.append(after_event[key]["runs"])
    afterevent_output_list.append(after_event[key]["balls"])

print("Leading from balls:\t" + "\t".join(map(str, afterevent_output_list)))

print("Runs per 6 ball segments:\t" + "\t".join(map(str, six_ball_segments)))

print("Before dismissal stats:\t" + "\t".join(
    map(str, [last_three_balls_score, final_ball])
))

for phase in phase_keys:
    phases_output_list.append(phases[phase]["runs"])
    phases_output_list.append(phases[phase]["balls"])

print("Match Stage Breakdown:\t" + "\t".join(map(str, phases_output_list)))

for pos in ball_position:
    ballno_output_list.append(ball_position[pos]["runs"])
    ballno_output_list.append(ball_position[pos]["balls"])

print("Ball in Over Breakdown:\t" + "\t".join(map(str, ballno_output_list)))

print(f"Boundary Balls: {boundary_balls}")

print("After dot streaks:\t" + "\t".join(map(str, [dot_streak_runs, dot_streak_balls])))
