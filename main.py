import json
from itertools import product

def check_time_overlaps(schedule):
    '''
    Check if there is any time overlap between two lists of tuples.
    Each tuple represents the start and end time of an event.
    '''
    for i in range(len(schedule[0])):
        for j in range(len(schedule[1])):
            if (schedule[0][i][0] < schedule[1][j][1] and schedule[0][i][1] > schedule[1][j][0]):
                return True
    return False

def convert_to_relative_time(day, time_in_minutes):
    '''
    Convert time in minutes to relative time from Monday 00:00
    '''
    day_offsets = {"M": 0, "T": 1440, "W": 2880, "Th": 4320, "F": 5760, "Sa": 7200, "Su": 8640}
    return day_offsets[day] + time_in_minutes

def check_if_overlap(course_one, course_two):
    '''
    Check if two courses overlap
    '''
    timings = [[], []]
    for key in ['LEC', 'SEM', 'LAB']:
        if key in course_one:
            for day in course_one[key]['date']:
                timing_tuple = (
                    convert_to_relative_time(day, course_one[key]['start']),
                    convert_to_relative_time(day, course_one[key]['end'])
                )
                timings[0].append(timing_tuple)
    for key in ['LEC', 'SEM', 'LAB']:
        if key in course_two:
            for day in course_two[key]['date']:
                timing_tuple = (
                    convert_to_relative_time(day, course_two[key]['start']),
                    convert_to_relative_time(day, course_two[key]['end'])
                )
                timings[1].append(timing_tuple)
    return check_time_overlaps(timings) 
        

def pretty_print_schedule(schedule):
    '''
    Print the schedule in a user-friendly format.
    '''
    days = ["M", "T", "W", "Th", "F", "Sa", "Su"]
    calendar = {day: [] for day in days}
    for course in schedule:
        course_id = course['id']
        for session_type in ['LEC', 'LAB', 'SEM']:
            if session_type in course:
                session = course[session_type]
                for day in session['date']:
                    start_time = session['start']
                    end_time = session['end']
                    start_str = f"{start_time // 60:02d}:{start_time % 60:02d}"
                    end_str = f"{end_time // 60:02d}:{end_time % 60:02d}"
                    calendar[day].append(f"{course_id} ({session_type}): {start_str} - {end_str}")
    print("\nWeekly Schedule:")
    print("=" * 40)
    for day in days:
        print(f"{day}:")
        if calendar[day]:
            for event in sorted(calendar[day]):
                print(f"  {event}")
        else:
            print("  No classes")
        print("-" * 40)
        
def main():
    course_codes = ["CIS*3190", "CIS*3700", "CIS*3760", "CIS*4520", "HROB*2010"]
    planner_with_sections = []

    with open('outputW25NoProfNoRooms.json', 'r') as file:
        data = json.load(file)

    for course in course_codes:
        if course in data:
            sections = data[course]['Sections']
            planner_with_sections.append(sections)

    planner_cartesian_product = product(*planner_with_sections)
    
    for item in planner_cartesian_product:
        is_valid = True
        for i, course_one in enumerate(item):
            for j, course_two in enumerate(item):
                if i < j and check_if_overlap(course_one, course_two):
                    is_valid = False
                    break
            if not is_valid:
                break
        if is_valid:
            pretty_print_schedule(item)

if __name__ == "__main__":
    main()
