from itertools import islice
def similar(a, b):
    """simple similarity check"""
    if len(a) < 2 or len(b) < 2:
        return 0
    
    # Quick length difference check
    if abs(len(a) - len(b)) > 2:
        return 0
    
    # Count matching characters
    matches = sum(1 for x, y in zip(a, b) if x == y)
    return matches / max(len(a), len(b)) if matches else 0

data = open('2021_public_sector_salary.csv')
all_data = data.readlines()  # Read all lines into memory
data.close()  # Close the file after reading

user_input = ''
while user_input != 'escape' and user_input != 'esc':
    print()
    print("Enter Name: (First) (Last)")
    user_input = input('> ')
    search_name = user_input.strip().split(' ')
    errors = 0
    total_results = 0
    results = []
    similar_results = []
    
    for person in all_data:
        try:
            personList = person.strip().split(',')

            agency = personList[0].strip()
            last_name = personList[1].strip("\"").strip()
            first_name = personList[2].strip("\"").strip().split(' ')[0]
            try:
                middle_initial = personList[2].strip("\"").strip().split(' ')[1]
            except:
                middle_initial = ''
            position = personList[3].strip()
            salary = personList[4].strip()
            sector = personList[7]

            if (first_name.lower() == search_name[0].lower() 
            and last_name.lower() == search_name[1].lower()):
                results.append(personList)
                total_results += 1
            elif (similar(first_name.lower(), search_name[0].lower()) + similar(last_name.lower(), search_name[1].lower())) > 1.4: # minimum similarity to be added to similar names list
                similar_results.append(f'{first_name.lower()} {last_name.lower()}')
        except:
            errors += 1
    if total_results == 0: #Possible outputs when 0 matches
        try:
            tempstring = f'\nThere are 0 results for {search_name[0].capitalize()} {search_name[1].capitalize()}'
            print(tempstring + '\n' + len(tempstring) * '-')
            if similar_results != []: #Sort based on similarity
                similar_results.sort(key=lambda x: similar(x, f'{search_name[0].lower()} {search_name[1].lower()}'))
                print('Did you mean: ', end="")
                print(', '.join(name.title() for name in islice(list(set(similar_results)),3)))
                print()
        except:
            print('Please use the format (First Name) (Last Name)')
    elif total_results == 1: #Print whole output when 1 result
        tempstring = f'\nThere is 1 result for {search_name[0].capitalize()} {search_name[1].capitalize()}:'
        print(tempstring + '\n' + len(tempstring) * '-')
        try:
            print(f'Name: {results[0][2].strip("\"").strip().split(' ')[0]} {results[0][2].strip("\"").strip().split(' ')[1]} {results[0][1].strip("\"").strip()}\nAgency: {results[0][0].strip()}\nPosition: {results[0][3].strip()}\nSalary: ${int(results[0][4].strip()):,}\nSector: {results[0][7].strip()}')
        except:
            print(f'Name: {results[0][2].strip("\"").strip().split(' ')[0]} {results[0][1].strip("\"").strip()}\nAgency: {results[0][0].strip()}\nPosition: {results[0][3].strip()}\nSalary: ${int(results[0][4].strip()):,}\nSector: {results[0][7].strip()}')
    else: #Offer selection of all possibilites when >1 result
        tempstring = f'\nThere are {total_results} results for {search_name[0].capitalize()} {search_name[1].capitalize()}:'
        print(tempstring + '\n' + len(tempstring) * '-')
        for result in results:
            i = results.index(result)
            try:
                print(f'[{i + 1}] {result[2].strip("\"").strip().split(' ')[0]} {result[2].strip("\"").strip().split(' ')[1]} {result[1].strip("\"").strip()} - {result[3].strip()}, {result[0].strip()}')
            except:
                print(f'[{i + 1}] {result[2].strip("\"").strip().split(' ')[0]} {result[1].strip("\"").strip()} - {result[3].strip()}, {result[0].strip()}')
        print(f'[{len(results) + 1}] Back')
        user_input = input('> ')
        while (user_input != 'bk') and (user_input != (str(len(results) + 1))) and (user_input != 'back'):
            try:
                if int(user_input) <= len(results) and int(user_input) > 0:
                    selected_person = results[int(user_input) - 1]
                    try:
                        print(f'Name: {selected_person[2].strip("\"").strip().split(' ')[0]} {selected_person[2].strip("\"").strip().split(' ')[1]} {selected_person[1].strip("\"").strip()}\nAgency: {selected_person[0].strip()}\nPosition: {selected_person[3].strip()}\nSalary: ${int(selected_person[4].strip()):,}\nSector: {selected_person[7].strip()}')
                    except:
                        print(f'Name: {selected_person[2].strip("\"").strip().split(' ')[0]} {selected_person[1].strip("\"").strip()}\nAgency: {selected_person[0].strip()}\nPosition: {selected_person[3].strip()}\nSalary: ${int(selected_person[4].strip()):,}\nSector: {selected_person[7].strip()}')
                    print()
            except:
                print(f'Please enter a valid selection (1-{len(results) + 1}) or a command')
            user_input = input('> ')