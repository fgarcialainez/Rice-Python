# template for "Stopwatch: The Game"
import simplegui

# define global variables
total_time = 0
timer_interval = 100 # 0.1 seconds
total_stops = 0
successful_stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenths = t % 10
    seconds = int(t / 10)
    
    tenths_str = str(tenths)
    minutes_str = str(int(seconds / 60))
    
    if seconds % 60 < 10:
        seconds_str = '0' + str(seconds % 60)
    else:
        seconds_str = str(seconds % 60)
    
    return minutes_str + ':' + seconds_str + '.' + tenths_str    

# creates the results string with the format x/y
def format_results():
    return str(successful_stops) + "/" + str(total_stops)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer
    if not timer.is_running():
        timer.start()

def stop():
    global timer, total_stops, successful_stops
    if timer.is_running():
        timer.stop()
        total_stops += 1
        
        # check successful stop
        if total_time % 10 == 0:
            successful_stops += 1
    
def reset():
    global timer, total_time, total_stops, successful_stops
    if timer.is_running():
        timer.stop()
        
    total_time = 0
    total_stops = 0
    successful_stops = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global total_time
    total_time += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(total_time), [60, 78], 34, "White")
    canvas.draw_text(format_results(), [160, 25], 22, "Green")
    
# create frame and timer
timer = simplegui.create_timer(timer_interval, timer_handler)

frame = simplegui.create_frame("Stopwatch: The Game", 200, 130)

# register event handlers
frame.add_button("Start", start, 120)
frame.add_button("Stop", stop, 120)
frame.add_button("Reset", reset, 120)

frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric