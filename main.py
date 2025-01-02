import json
from itertools import product

def check_time_overlaps(schedule):
    '''
    Check if there is any time overlap between two lists of tuples.
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

def get_course_timings_list(course):
    """
    Extract all timings (LEC, LAB, SEM) for a course as a list of tuples.
    """
    timings = []
    for key in ['LEC', 'SEM', 'LAB']:
        if key in course:
            for day in course[key]['date']:
                timings.append((convert_to_relative_time(day, course[key]['start']),convert_to_relative_time(day, course[key]['end'])))
    return timings

def pretty_print_schedule(schedule):
    '''
    Print the schedule in a user-friendly format.
    '''
    days = ["M", "T", "W", "Th", "F", "Sa", "Su"]
    calendar = {day: [] for day in days}
    for course in schedule:
        for session_type in ['LEC', 'LAB', 'SEM']:
            if session_type in course:
                for day in course[session_type]['date']:
                    calendar[day].append(f"{course['id']} ({session_type}): { course[session_type]['start'] // 60:02d}:{ course[session_type]['start'] % 60:02d} - { course[session_type]['end'] // 60:02d}:{ course[session_type]['end'] % 60:02d}")
    for day in days:
        print(f"{day}:")
        if calendar[day]:
            for event in calendar[day]:
                print(f"\t{event}")
    print("-" * 50, '\n')
        
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
                if i < j and check_time_overlaps([get_course_timings_list(course_one), get_course_timings_list(course_two)]):
                    is_valid = False
                    break
            if not is_valid:
                break
        if is_valid:
            pretty_print_schedule(item)

if __name__ == "__main__":
    main()
